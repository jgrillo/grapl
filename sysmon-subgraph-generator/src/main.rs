#[macro_use]
extern crate lazy_static;

extern crate aws_lambda_events;
extern crate chrono;
extern crate failure;
extern crate futures;
extern crate graph_descriptions;
extern crate graph_generator_lib;
extern crate lambda_runtime as lambda;
extern crate log;
extern crate rayon;
extern crate regex;
extern crate rusoto_core;
extern crate rusoto_s3;
extern crate rusoto_sqs;
extern crate serde;
//extern crate simple_logger;

extern crate env_logger;

extern crate sqs_lambda;
extern crate stopwatch;
extern crate sysmon;
extern crate uuid;
extern crate zstd;

use async_trait::async_trait;
use std::borrow::Cow;
use std::marker::PhantomData;
use std::sync::Arc;
use std::str::FromStr;
use aws_lambda_events::event::sqs::{SqsEvent, SqsMessage};
use chrono::prelude::*;
use failure::bail;
use failure::Error;
use futures::{Future, Stream};
use graph_descriptions::*;
use graph_descriptions::graph_description::*;
use graph_generator_lib::upload_subgraphs;
use lambda::Context;
use lambda::error::HandlerError;
use lambda::Handler;
use lambda::lambda;
use log::*;
use log::error;
use rayon::iter::Either;
use rayon::prelude::*;
use rusoto_core::Region;
use rusoto_s3::{GetObjectRequest, S3};
use rusoto_s3::S3Client;
use rusoto_sqs::{GetQueueUrlRequest, Sqs, SqsClient};
use serde::Deserialize;
use sysmon::*;
use regex::Regex;
use uuid::Uuid;
use prost::Message;

use sqs_completion_handler::*;
use sqs_consumer::*;
use sqs_lambda::completion_event_serializer::CompletionEventSerializer;
use sqs_lambda::event_decoder::PayloadDecoder;
use sqs_lambda::event_emitter::S3EventEmitter;
use sqs_lambda::event_handler::EventHandler;
use sqs_lambda::event_processor;
use sqs_lambda::event_retriever::S3PayloadRetriever;
use sqs_lambda::sqs_completion_handler;
use sqs_lambda::sqs_consumer;
use std::time::{Duration, UNIX_EPOCH, SystemTime};
use sqs_lambda::event_processor::{EventProcessorActor, EventProcessor};
use std::io::Cursor;
use aws_lambda_events::event::s3::S3Event;


macro_rules! log_time {
    ($msg:expr, $x:expr) => {
        {
            let mut sw = stopwatch::Stopwatch::start_new();
            #[allow(path_statements)]
            let result = $x;
            sw.stop();
            info!("{} {} milliseconds", $msg, sw.elapsed_ms());
            result
        }
    };
}

fn strip_file_zone_identifier(path: &str) -> &str {
    if path.ends_with(":Zone.Identifier") {
        &path[0..path.len() - ":Zone.Identifier".len()]
    } else {
        path
    }
}

fn is_internal_ip(ip: &str) -> bool {
    lazy_static!(
        static ref RE: Regex = Regex::new(
            r"/(^127\.)|(^192\.168\.)|(^10\.)|(^172\.1[6-9]\.)|(^172\.2[0-9]\.)|(^172\.3[0-1]\.)|(^::1$)|(^[fF][cCdD])/"
        ).expect("is_internal_ip regex");
    );

    RE.is_match(ip)
}

fn get_image_name(image_path: &str) -> Option<String> {
    image_path.split("\\").last().map(|name| {
        name.replace("- ", "").replace("\\", "")
    })
}

pub fn utc_to_epoch(utc: &str) -> Result<u64, Error> {
    let dt = NaiveDateTime::parse_from_str(
        utc, "%Y-%m-%d %H:%M:%S%.3f")?;

    let dt: DateTime<Utc> = DateTime::from_utc(dt, Utc);
    let ts = dt.timestamp_millis();

    if ts < 0 {
        bail!("Timestamp is negative")
    }

    Ok(ts as u64)
}

fn handle_process_start(process_start: &ProcessCreateEvent) -> Result<GraphDescription, Error> {
    let timestamp = utc_to_epoch(&process_start.event_data.utc_time)?;
    let mut graph = GraphDescription::new(
        timestamp
    );

//    let asset = AssetDescriptionBuilder::default();

    let parent = ProcessDescriptionBuilder::default()
        .asset_id(process_start.system.computer.computer.clone())
        .state(ProcessState::Existing)
        .process_id(process_start.event_data.parent_process_id)
        .process_name(get_image_name(&process_start.event_data.parent_image.clone()).unwrap())
        .process_command_line(&process_start.event_data.parent_command_line.command_line)
        .last_seen_timestamp(timestamp)
        .created_timestamp(process_start.event_data.parent_process_guid.get_creation_timestamp())
        .build()
        .unwrap();

    let child = ProcessDescriptionBuilder::default()
        .asset_id(process_start.system.computer.computer.clone())
        .process_name(get_image_name(&process_start.event_data.image.clone()).unwrap())
        .process_command_line(&process_start.event_data.command_line.command_line)
        .state(ProcessState::Created)
        .process_id(process_start.event_data.process_id)
        .created_timestamp(timestamp)
        .build()
        .unwrap();

    let child_exe = FileDescriptionBuilder::default()
        .asset_id(process_start.system.computer.computer.clone())
        .state(FileState::Existing)
        .last_seen_timestamp(timestamp)
        .file_path(strip_file_zone_identifier(&process_start.event_data.image))
        .build()
        .unwrap();

    graph.add_edge("bin_file",
                   child.clone_key(),
                   child_exe.clone_key(),
    );

    graph.add_node(child_exe);

    graph.add_edge("children",
                   parent.clone_key(),
                   child.clone_key());
    graph.add_node(parent);
    graph.add_node(child);

    Ok(graph)
}

fn handle_file_create(file_create: &FileCreateEvent) -> Result<GraphDescription, Error> {
    let timestamp = utc_to_epoch(&file_create.event_data.creation_utc_time)?;
    let mut graph = GraphDescription::new(
        timestamp
    );

    let creator = ProcessDescriptionBuilder::default()
        .asset_id(file_create.system.computer.computer.clone())
        .state(ProcessState::Existing)
        .process_id(file_create.event_data.process_id)
        .process_name(get_image_name(&file_create.event_data.image.clone()).unwrap())
        .last_seen_timestamp(timestamp)
        .created_timestamp(file_create.event_data.process_guid.get_creation_timestamp())
        .build()
        .unwrap();

    let file = FileDescriptionBuilder::default()
        .asset_id(file_create.system.computer.computer.clone())
        .state(FileState::Created)
        .file_path(strip_file_zone_identifier(&file_create.event_data.target_filename))
        .created_timestamp(timestamp)
        .build()
        .unwrap();


    graph.add_edge("created_files",
                   creator.clone_key(),
                   file.clone_key());
    graph.add_node(creator);
    graph.add_node(file);

    Ok(graph)
}


fn handle_inbound_connection(inbound_connection: &NetworkEvent) -> Result<GraphDescription, Error> {
    let timestamp = utc_to_epoch(&inbound_connection.event_data.utc_time)?;
    let mut graph = GraphDescription::new(
        timestamp
    );

    if inbound_connection.event_data.source_hostname.is_none() {
        warn!("inbound connection source hostname is empty")
    }

    let process = ProcessDescriptionBuilder::default()
        .hostname(inbound_connection.event_data.source_hostname.clone())
        .state(ProcessState::Existing)
        .process_id(inbound_connection.event_data.process_id)
        .process_name(get_image_name(&inbound_connection.event_data.image).unwrap())
        .last_seen_timestamp(timestamp)
        .created_timestamp(inbound_connection.event_data.process_guid.get_creation_timestamp())
        .build()
        .unwrap();

    // Inbound is the 'src', at least in sysmon
    let inbound = InboundConnectionBuilder::default()
        .hostname(inbound_connection.event_data.source_hostname.clone())
        .state(ConnectionState::Created)
        .port(inbound_connection.event_data.source_port)
        .created_timestamp(timestamp)
        .build()
        .unwrap();

    if is_internal_ip(&inbound_connection.event_data.destination_ip.clone()) {
        if inbound_connection.event_data.source_hostname.is_none() {
            warn!("inbound connection dest hostname is empty")
        }

        let outbound = InboundConnectionBuilder::default()
            .hostname(inbound_connection.event_data.destination_hostname.clone())
            .state(ConnectionState::Created)
            .port(inbound_connection.event_data.source_port)
            .created_timestamp(timestamp)
            .build()
            .unwrap();

        graph.add_edge("connection",
                       outbound.clone_key(),
                       inbound.clone_key());

        graph.add_node(outbound);
    } else {
        info!("Handling external ip {}", inbound_connection.event_data.destination_ip.clone());

        let external_ip = IpAddressDescription::new(
            timestamp,
            inbound_connection.event_data.destination_ip.clone(),
            &inbound_connection.event_data.protocol,
        );

        graph.add_edge("external_connection",
                       inbound.clone_key(),
                       external_ip.clone_key());

        graph.add_node(external_ip);
    }

    graph.add_edge("bound_connection",
                   process.clone_key(),
                   inbound.clone_key());

    graph.add_node(inbound);
    graph.add_node(process);

    info!("handle_inbound_connection");

    Ok(graph)
}


fn handle_outbound_connection(outbound_connection: &NetworkEvent) -> Result<GraphDescription, Error> {
    let timestamp = utc_to_epoch(&outbound_connection.event_data.utc_time)?;

    let mut graph = GraphDescription::new(
        timestamp
    );

    if outbound_connection.event_data.source_hostname.is_none() {
        warn!("outbound connection source hostname is empty")
    }

    // A process creates an outbound connection to dst_port
    // Another process must have an inbound connection to src_port
    // Or the other process is external/ not running the instrumentation
    let process = ProcessDescriptionBuilder::default()
        .asset_id(outbound_connection.event_data.source_hostname.to_owned())
        .state(ProcessState::Existing)
        .process_id(outbound_connection.event_data.process_id)
        .process_name(get_image_name(&outbound_connection.event_data.image.clone()).unwrap())
        .last_seen_timestamp(timestamp)
        .created_timestamp(outbound_connection.event_data.process_guid.get_creation_timestamp())
        .build()
        .unwrap();

    let outbound = OutboundConnectionBuilder::default()
        .asset_id(outbound_connection.event_data.source_hostname.to_owned())
        .state(ConnectionState::Created)
        .port(outbound_connection.event_data.source_port)
        .created_timestamp(timestamp)
        .build()
        .unwrap();


    if is_internal_ip(&outbound_connection.event_data.destination_ip.to_owned()) {
        bail!("Internal IP not supported");
//        let inbound = if outbound_connection.destination_hostname.is_empty() {
//            warn!("outbound connection dest hostname is empty {:?}", outbound_connection);
//            InboundConnectionBuilder::default()
//                .state(ConnectionState::Existing)
//                .port(outbound_connection.destination_port)
//                .last_seen_timestamp(timestamp)
//                .hostname(outbound_connection.destination_hostname.to_owned())
//                .build()
//                .unwrap()
//        } else {
//            InboundConnectionBuilder::default()
//                .state(ConnectionState::Existing)
//                .port(outbound_connection.destination_port)
//                .last_seen_timestamp(timestamp)
//                .host_ip(outbound_connection.destination_ip.to_owned())
//                .build()
//                .unwrap()
//        };
//
//        graph.add_edge("connection",
//                       outbound.clone_key(),
//                       inbound.clone_key());
//        graph.add_node(inbound);
    } else {
        info!("Handling external ip {}", outbound_connection.event_data.destination_ip.to_owned());

        let external_ip = IpAddressDescription::new(
            timestamp,
            outbound_connection.event_data.destination_ip.to_owned(),
            &outbound_connection.event_data.protocol,
        );

        graph.add_edge("external_connection",
                       outbound.clone_key(),
                       external_ip.clone_key());

        graph.add_node(external_ip);
    }

    graph.add_edge("created_connection",
                   process.clone_key(),
                   outbound.clone_key());


    graph.add_node(outbound);
    graph.add_node(process);

    info!("handle_outbound_connection");
    Ok(graph)
}

fn time_based_key_fn(_event: &[u8]) -> String {
    let cur_ms = match SystemTime::now().duration_since(UNIX_EPOCH) {
        Ok(n) => n.as_millis(),
        Err(_) => panic!("SystemTime before UNIX EPOCH!"),
    };

    let cur_day = cur_ms - (cur_ms % 86400);

    format!(
        "{}/{}-{}",
        cur_day, cur_ms, uuid::Uuid::new_v4()
    )
}

#[derive(Clone, Debug, Default)]
pub struct SubgraphSerializer {
    proto: Vec<u8>,
}

impl CompletionEventSerializer for SubgraphSerializer {
    type CompletedEvent = GeneratedSubgraphs;
    type Output = Vec<u8>;
    type Error = failure::Error;

    fn serialize_completed_events(
        &mut self,
        completed_events: &[Self::CompletedEvent],
    ) -> Result<Self::Output, Self::Error> {
        let mut subgraph = GraphDescription::new(
            0
        );

        for completed_event in completed_events {
            for sg in completed_event.subgraphs.iter() {
                subgraph.merge(sg);
            }
        }

        let subgraphs = GeneratedSubgraphs {subgraphs: vec![subgraph]};

        self.proto.clear();

        subgraphs.encode(&mut self.proto)?;


        let mut compressed = Vec::with_capacity(self.proto.len());
        let mut proto = Cursor::new(&self.proto);
        zstd::stream::copy_encode(&mut proto, &mut compressed, 4)?;

        Ok(compressed)

    }
}

#[derive(Clone, Default)]
pub struct ZstdDecoder {
    pub buffer: Vec<u8>
}

impl PayloadDecoder<Vec<u8>> for ZstdDecoder
{
    fn decode(&mut self, body: Vec<u8>) -> Result<Vec<u8>, Box<dyn std::error::Error>>
    {
        self.buffer.clear();

        let mut body = Cursor::new(&body);

        zstd::stream::copy_decode(&mut body, &mut self.buffer)?;

        Ok(self.buffer.clone())
    }
}

struct SysmonSubgraphGenerator
{}

impl Clone for SysmonSubgraphGenerator

{
    fn clone(&self) -> Self {
        Self {}
    }
}


impl SysmonSubgraphGenerator

{
    pub fn new() -> Self {
        Self {}
    }
}

#[async_trait]
impl EventHandler for SysmonSubgraphGenerator

{
    type InputEvent = Vec<u8>;
    type OutputEvent = GeneratedSubgraphs;
    type Error = failure::Error;

    async fn handle_event(&mut self, event: Vec<u8>) -> Result<Self::OutputEvent, Error> {
        info!("Handling raw event");

        let events: Vec<_> = log_time!(
            "event split",
            event.split(|i| &[*i][..] == &b"\n"[..]).collect()
        );

        let subgraphs: Vec<_> = log_time!(
            "events par_iter",
             events.into_par_iter().flat_map(move |event| {
                let event = String::from_utf8_lossy(event);
                let event = Event::from_str(&event);
                let event = event.ok()?;

                match event {
                    Event::ProcessCreate(event) => {
                        info!("Handling process create");
                        match handle_process_start(&event) {
                            Ok(event) => Some(event),
                            Err(e) => {
                                warn!("Failed to process process start event: {}", e);
                                None
                            }
                        }
                    }
                    Event::FileCreate(event) => {
                        info!("FileCreate");
                        match handle_file_create(&event) {
                            Ok(event) => Some(event),
                            Err(e) => {
                                warn!("Failed to process file create event: {}", e);
                                None
                            }
                        }
                    }
//                    Event::InboundNetwork(event) => {
//                        match handle_inbound_connection(event) {
//                            Ok(event) => Some(event),
//                            Err(e) => {
//                                warn!("Failed to process inbound network event: {}", e);
//                                None
//                            }
//                        }
//                    }
                    Event::OutboundNetwork(event) => {
                        match handle_outbound_connection(&event) {
                            Ok(event) => Some(event),
                            Err(e) => {
                                warn!("Failed to process outbound network event: {}", e);
                                None
                            }
                        }
                    }
                    catch => {warn!("Unsupported event_type: {:?}", catch); None}
                }
            }).collect()
        );

        info!("Completed mapping {} subgraphs", subgraphs.len());
        let graphs = GeneratedSubgraphs { subgraphs };

        Ok(graphs)
    }
}

//
//fn my_handler(event: SqsEvent, ctx: Context) -> Result<(), HandlerError> {
//    let region = {
//        let region_str = std::env::var("AWS_REGION").expect("AWS_REGION");
//        Region::from_str(&region_str).expect("Region error")
//    };
//
//    info!("Creating sqs_client");
//    let sqs_client = Arc::new(SqsClient::new(region.clone()));
//
//    info!("Creating s3_client");
//    let s3_client = Arc::new(S3Client::new(region.clone()));
//
//    info!("Creating retriever");
//    let retriever = S3PayloadRetriever::new(
//        s3_client.clone(),
//        |d| {info!("Parsing: {:?}", d); events_from_s3_sns_sqs(d)},
//        ZstdDecoder{buffer: Vec::with_capacity(1 << 8)},
//    );
//
//    let queue_url = std::env::var("QUEUE_URL").expect("QUEUE_URL");
//
//    info!("Creating sqs_completion_handler");
//    let sqs_completion_handler = NopSqsCompletionHandler::new(
//        queue_url
//    );
//
//    let handler = SysmonSubgraphGenerator::new(
//        move |generated_subgraphs| {
//            upload_subgraphs(s3_client.as_ref(), generated_subgraphs)
//        }
//    );
//
//    let mut sqs_service = SqsService::new(
//        retriever,
//        handler,
//        sqs_completion_handler,
//    );
//
//    info!("Handing off event");
//    sqs_service.run(event, ctx)?;
//
//    Ok(())
//}

fn map_sqs_message(event: aws_lambda_events::event::sqs::SqsMessage) -> rusoto_sqs::Message {
    rusoto_sqs::Message {
        attributes: Some(event.attributes),
        body: event.body,
        md5_of_body: event.md5_of_body,
        md5_of_message_attributes: event.md5_of_message_attributes,
        message_attributes: None,
        message_id: event.message_id,
        receipt_handle: event.receipt_handle
    }
}



fn my_handler(event: SqsEvent, ctx: Context) -> Result<(), HandlerError> {
    info!("Handling event");

    tokio_compat::run_std(
        async {

            let queue_url = std::env::var("QUEUE_URL").expect("QUEUE_URL");
            info!("Queue Url: {}", queue_url);
            let bucket_prefix = std::env::var("BUCKET_PREFIX").expect("BUCKET_PREFIX");

            let bucket = bucket_prefix + "-unid-subgraphs-generated-bucket";
            info!("Output events to: {}", bucket);
            let region = {
                let region_str = std::env::var("AWS_REGION").expect("AWS_REGION");
                Region::from_str(&region_str).expect("Region error")
            };

            info!("SqsCompletionHandler");
            let sqs_completion_handler = SqsCompletionHandlerActor::new(
                SqsCompletionHandler::new(
                    SqsClient::new(region.clone()),
                    queue_url.to_string(),
                    SubgraphSerializer { proto: Vec::with_capacity(1024) },
                    S3EventEmitter::new(
                        S3Client::new(region.clone()),
                        bucket.to_owned(),
                        time_based_key_fn,
                    ),
                    CompletionPolicy::new(
                        1000, // Buffer up to 1000 messages
                        Duration::from_secs(30), // Buffer for up to 30 seconds
                    ),
                )
            );


            info!("Defining consume policy");
            let consume_policy = ConsumePolicy::new(
                ctx, // Use the Context.deadline from the lambda_runtime
                Duration::from_secs(2), // Stop consuming when there's 2 seconds left in the runtime
                3, // If we get 3 empty receives in a row, stop consuming
            );

            info!("Defining consume policy");
            let (tx, shutdown_notify) = tokio::sync::oneshot::channel();

            info!("SqsConsumer");
            let sqs_consumer = SqsConsumerActor::new(
                SqsConsumer::new(
                    SqsClient::new(region.clone()),
                    queue_url.clone(),
                    consume_policy,
                    sqs_completion_handler.clone(),
                    tx
                )
            );

            info!("EventProcessors");
            let event_processors: Vec<_> = (0..40)
                .map(|_| {
                    EventProcessorActor::new(EventProcessor::new(
                        sqs_consumer.clone(),
                        sqs_completion_handler.clone(),
                        SysmonSubgraphGenerator {},
                        S3PayloadRetriever::new(S3Client::new(region.clone()), ZstdDecoder::default()),
                    ))
                })
                .collect();

            info!("Start Processing");

            futures::future::join_all(event_processors.iter().map(|ep| ep.start_processing())).await;

            let mut proc_iter = event_processors.iter().cycle();
            for event in event.records {
                let next_proc = proc_iter.next().unwrap();
                next_proc.process_event(
                    map_sqs_message(event)
                ).await;
            }

            info!("Waiting for shutdown notification");
            // Wait for the consumers to shutdown
            let _ = shutdown_notify.await;

            tokio::time::delay_for(Duration::from_millis(100)).await;
            info!("Consumer shutdown");

        });


    info!("Completed execution");
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    env_logger::init(); // This initializes the `env_logger`

    info!("Starting lambda");
    lambda!(my_handler);
    Ok(())
}


#[cfg(test)]
mod tests {
    use super::*;
    use rusoto_s3::CreateBucketRequest;
    use std::time::Duration;
    use rusoto_core::credential::StaticProvider;
    use rusoto_core::HttpClient;

    #[test]
    fn parse_time() {
        let utc_time = "2017-04-28 22:08:22.025";
        let ts = utc_to_epoch(utc_time).expect("parsing utc_time failed");
        println!("{}", ts);
    }

    #[test]
    fn test_handler() {
        let region = Region::Custom {
            name: "us-east-1".to_string(),
            endpoint: "http://127.0.0.1:9000".to_string(),
        };

        std::env::set_var("BUCKET_PREFIX", "unique_id");

        let handler = SysmonSubgraphGenerator::new(
            move |generated_subgraphs| {
                println!("generated subgraphs");
                Ok(())
            }
        );

        handler.handle_event(vec![]).expect("handle_event failed");
    }
}

