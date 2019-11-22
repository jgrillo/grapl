# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
    RepeatedScalarFieldContainer as google___protobuf___internal___containers___RepeatedScalarFieldContainer,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from google.protobuf.wrappers_pb2 import (
    StringValue as google___protobuf___wrappers_pb2___StringValue,
)

from typing import (
    Iterable as typing___Iterable,
    Mapping as typing___Mapping,
    MutableMapping as typing___MutableMapping,
    Optional as typing___Optional,
    Text as typing___Text,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int


class Host(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    hostname = ... # type: typing___Text
    ip = ... # type: typing___Text
    asset_id = ... # type: typing___Text

    def __init__(self,
        *,
        hostname : typing___Optional[typing___Text] = None,
        ip : typing___Optional[typing___Text] = None,
        asset_id : typing___Optional[typing___Text] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> Host: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"asset_id",u"host_id",u"hostname",u"ip"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"asset_id",u"host_id",u"hostname",u"ip"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"asset_id",b"asset_id",u"host_id",b"host_id",u"hostname",b"hostname",u"ip",b"ip"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"asset_id",b"asset_id",u"host_id",b"host_id",u"hostname",b"hostname",u"ip",b"ip"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions___Literal[u"host_id",b"host_id"]) -> typing_extensions___Literal["hostname","ip","asset_id"]: ...

class AssetDescription(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    node_key = ... # type: typing___Text
    timestamp = ... # type: builtin___int
    operating_system = ... # type: typing___Text

    @property
    def asset_id(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    @property
    def host_name(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    @property
    def host_domain(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    @property
    def host_fqdn(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    @property
    def host_local_mac(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    @property
    def host_ip(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    def __init__(self,
        *,
        node_key : typing___Optional[typing___Text] = None,
        timestamp : typing___Optional[builtin___int] = None,
        asset_id : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        host_name : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        host_domain : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        host_fqdn : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        host_local_mac : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        host_ip : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        operating_system : typing___Optional[typing___Text] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> AssetDescription: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"asset_id",u"host_domain",u"host_fqdn",u"host_ip",u"host_local_mac",u"host_name"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"asset_id",u"host_domain",u"host_fqdn",u"host_ip",u"host_local_mac",u"host_name",u"node_key",u"operating_system",u"timestamp"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"asset_id",b"asset_id",u"host_domain",b"host_domain",u"host_fqdn",b"host_fqdn",u"host_ip",b"host_ip",u"host_local_mac",b"host_local_mac",u"host_name",b"host_name"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"asset_id",b"asset_id",u"host_domain",b"host_domain",u"host_fqdn",b"host_fqdn",u"host_ip",b"host_ip",u"host_local_mac",b"host_local_mac",u"host_name",b"host_name",u"node_key",b"node_key",u"operating_system",b"operating_system",u"timestamp",b"timestamp"]) -> None: ...

class NodeDescription(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def asset_node(self) -> AssetDescription: ...

    @property
    def process_node(self) -> ProcessDescription: ...

    @property
    def file_node(self) -> FileDescription: ...

    @property
    def ip_address_node(self) -> IpAddressDescription: ...

    @property
    def outbound_connection_node(self) -> OutboundConnection: ...

    @property
    def inbound_connection_node(self) -> InboundConnection: ...

    @property
    def dynamic_node(self) -> DynamicNode: ...

    def __init__(self,
        *,
        asset_node : typing___Optional[AssetDescription] = None,
        process_node : typing___Optional[ProcessDescription] = None,
        file_node : typing___Optional[FileDescription] = None,
        ip_address_node : typing___Optional[IpAddressDescription] = None,
        outbound_connection_node : typing___Optional[OutboundConnection] = None,
        inbound_connection_node : typing___Optional[InboundConnection] = None,
        dynamic_node : typing___Optional[DynamicNode] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> NodeDescription: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"asset_node",u"dynamic_node",u"file_node",u"inbound_connection_node",u"ip_address_node",u"outbound_connection_node",u"process_node",u"which_node"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"asset_node",u"dynamic_node",u"file_node",u"inbound_connection_node",u"ip_address_node",u"outbound_connection_node",u"process_node",u"which_node"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"asset_node",b"asset_node",u"dynamic_node",b"dynamic_node",u"file_node",b"file_node",u"inbound_connection_node",b"inbound_connection_node",u"ip_address_node",b"ip_address_node",u"outbound_connection_node",b"outbound_connection_node",u"process_node",b"process_node",u"which_node",b"which_node"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"asset_node",b"asset_node",u"dynamic_node",b"dynamic_node",u"file_node",b"file_node",u"inbound_connection_node",b"inbound_connection_node",u"ip_address_node",b"ip_address_node",u"outbound_connection_node",b"outbound_connection_node",u"process_node",b"process_node",u"which_node",b"which_node"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions___Literal[u"which_node",b"which_node"]) -> typing_extensions___Literal["asset_node","process_node","file_node","ip_address_node","outbound_connection_node","inbound_connection_node","dynamic_node"]: ...

class OutboundConnection(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    node_key = ... # type: typing___Text
    state = ... # type: builtin___int
    created_timestamp = ... # type: builtin___int
    terminated_timestamp = ... # type: builtin___int
    last_seen_timestamp = ... # type: builtin___int
    port = ... # type: builtin___int

    @property
    def asset_id(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    @property
    def hostname(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    @property
    def host_ip(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    def __init__(self,
        *,
        node_key : typing___Optional[typing___Text] = None,
        asset_id : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        hostname : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        host_ip : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        state : typing___Optional[builtin___int] = None,
        created_timestamp : typing___Optional[builtin___int] = None,
        terminated_timestamp : typing___Optional[builtin___int] = None,
        last_seen_timestamp : typing___Optional[builtin___int] = None,
        port : typing___Optional[builtin___int] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> OutboundConnection: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"asset_id",u"host_ip",u"hostname"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"asset_id",u"created_timestamp",u"host_ip",u"hostname",u"last_seen_timestamp",u"node_key",u"port",u"state",u"terminated_timestamp"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"asset_id",b"asset_id",u"host_ip",b"host_ip",u"hostname",b"hostname"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"asset_id",b"asset_id",u"created_timestamp",b"created_timestamp",u"host_ip",b"host_ip",u"hostname",b"hostname",u"last_seen_timestamp",b"last_seen_timestamp",u"node_key",b"node_key",u"port",b"port",u"state",b"state",u"terminated_timestamp",b"terminated_timestamp"]) -> None: ...

class InboundConnection(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    node_key = ... # type: typing___Text
    state = ... # type: builtin___int
    created_timestamp = ... # type: builtin___int
    terminated_timestamp = ... # type: builtin___int
    last_seen_timestamp = ... # type: builtin___int
    port = ... # type: builtin___int

    @property
    def asset_id(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    @property
    def hostname(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    @property
    def host_ip(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    def __init__(self,
        *,
        node_key : typing___Optional[typing___Text] = None,
        asset_id : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        hostname : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        host_ip : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        state : typing___Optional[builtin___int] = None,
        created_timestamp : typing___Optional[builtin___int] = None,
        terminated_timestamp : typing___Optional[builtin___int] = None,
        last_seen_timestamp : typing___Optional[builtin___int] = None,
        port : typing___Optional[builtin___int] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> InboundConnection: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"asset_id",u"host_ip",u"hostname"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"asset_id",u"created_timestamp",u"host_ip",u"hostname",u"last_seen_timestamp",u"node_key",u"port",u"state",u"terminated_timestamp"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"asset_id",b"asset_id",u"host_ip",b"host_ip",u"hostname",b"hostname"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"asset_id",b"asset_id",u"created_timestamp",b"created_timestamp",u"host_ip",b"host_ip",u"hostname",b"hostname",u"last_seen_timestamp",b"last_seen_timestamp",u"node_key",b"node_key",u"port",b"port",u"state",b"state",u"terminated_timestamp",b"terminated_timestamp"]) -> None: ...

class ProcessDescription(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    node_key = ... # type: typing___Text
    state = ... # type: builtin___int
    process_id = ... # type: builtin___int
    process_guid = ... # type: typing___Text
    created_timestamp = ... # type: builtin___int
    terminated_timestamp = ... # type: builtin___int
    last_seen_timestamp = ... # type: builtin___int
    process_name = ... # type: typing___Text
    process_command_line = ... # type: typing___Text
    process_integrity_level = ... # type: typing___Text
    operating_system = ... # type: typing___Text

    @property
    def asset_id(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    @property
    def hostname(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    @property
    def host_ip(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    def __init__(self,
        *,
        node_key : typing___Optional[typing___Text] = None,
        asset_id : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        hostname : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        host_ip : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        state : typing___Optional[builtin___int] = None,
        process_id : typing___Optional[builtin___int] = None,
        process_guid : typing___Optional[typing___Text] = None,
        created_timestamp : typing___Optional[builtin___int] = None,
        terminated_timestamp : typing___Optional[builtin___int] = None,
        last_seen_timestamp : typing___Optional[builtin___int] = None,
        process_name : typing___Optional[typing___Text] = None,
        process_command_line : typing___Optional[typing___Text] = None,
        process_integrity_level : typing___Optional[typing___Text] = None,
        operating_system : typing___Optional[typing___Text] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> ProcessDescription: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"asset_id",u"host_ip",u"hostname"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"asset_id",u"created_timestamp",u"host_ip",u"hostname",u"last_seen_timestamp",u"node_key",u"operating_system",u"process_command_line",u"process_guid",u"process_id",u"process_integrity_level",u"process_name",u"state",u"terminated_timestamp"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"asset_id",b"asset_id",u"host_ip",b"host_ip",u"hostname",b"hostname"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"asset_id",b"asset_id",u"created_timestamp",b"created_timestamp",u"host_ip",b"host_ip",u"hostname",b"hostname",u"last_seen_timestamp",b"last_seen_timestamp",u"node_key",b"node_key",u"operating_system",b"operating_system",u"process_command_line",b"process_command_line",u"process_guid",b"process_guid",u"process_id",b"process_id",u"process_integrity_level",b"process_integrity_level",u"process_name",b"process_name",u"state",b"state",u"terminated_timestamp",b"terminated_timestamp"]) -> None: ...

class FileDescription(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    node_key = ... # type: typing___Text
    state = ... # type: builtin___int
    created_timestamp = ... # type: builtin___int
    deleted_timestamp = ... # type: builtin___int
    last_seen_timestamp = ... # type: builtin___int
    file_name = ... # type: typing___Text
    file_path = ... # type: typing___Text
    file_extension = ... # type: typing___Text
    file_mime_type = ... # type: typing___Text
    file_size = ... # type: builtin___int
    file_version = ... # type: typing___Text
    file_description = ... # type: typing___Text
    file_product = ... # type: typing___Text
    file_company = ... # type: typing___Text
    file_directory = ... # type: typing___Text
    file_inode = ... # type: builtin___int
    file_hard_links = ... # type: builtin___int
    md5_hash = ... # type: typing___Text
    sha1_hash = ... # type: typing___Text
    sha256_hash = ... # type: typing___Text

    @property
    def asset_id(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    @property
    def hostname(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    @property
    def host_ip(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    def __init__(self,
        *,
        node_key : typing___Optional[typing___Text] = None,
        asset_id : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        hostname : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        host_ip : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        state : typing___Optional[builtin___int] = None,
        created_timestamp : typing___Optional[builtin___int] = None,
        deleted_timestamp : typing___Optional[builtin___int] = None,
        last_seen_timestamp : typing___Optional[builtin___int] = None,
        file_name : typing___Optional[typing___Text] = None,
        file_path : typing___Optional[typing___Text] = None,
        file_extension : typing___Optional[typing___Text] = None,
        file_mime_type : typing___Optional[typing___Text] = None,
        file_size : typing___Optional[builtin___int] = None,
        file_version : typing___Optional[typing___Text] = None,
        file_description : typing___Optional[typing___Text] = None,
        file_product : typing___Optional[typing___Text] = None,
        file_company : typing___Optional[typing___Text] = None,
        file_directory : typing___Optional[typing___Text] = None,
        file_inode : typing___Optional[builtin___int] = None,
        file_hard_links : typing___Optional[builtin___int] = None,
        md5_hash : typing___Optional[typing___Text] = None,
        sha1_hash : typing___Optional[typing___Text] = None,
        sha256_hash : typing___Optional[typing___Text] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> FileDescription: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"asset_id",u"host_ip",u"hostname"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"asset_id",u"created_timestamp",u"deleted_timestamp",u"file_company",u"file_description",u"file_directory",u"file_extension",u"file_hard_links",u"file_inode",u"file_mime_type",u"file_name",u"file_path",u"file_product",u"file_size",u"file_version",u"host_ip",u"hostname",u"last_seen_timestamp",u"md5_hash",u"node_key",u"sha1_hash",u"sha256_hash",u"state"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"asset_id",b"asset_id",u"host_ip",b"host_ip",u"hostname",b"hostname"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"asset_id",b"asset_id",u"created_timestamp",b"created_timestamp",u"deleted_timestamp",b"deleted_timestamp",u"file_company",b"file_company",u"file_description",b"file_description",u"file_directory",b"file_directory",u"file_extension",b"file_extension",u"file_hard_links",b"file_hard_links",u"file_inode",b"file_inode",u"file_mime_type",b"file_mime_type",u"file_name",b"file_name",u"file_path",b"file_path",u"file_product",b"file_product",u"file_size",b"file_size",u"file_version",b"file_version",u"host_ip",b"host_ip",u"hostname",b"hostname",u"last_seen_timestamp",b"last_seen_timestamp",u"md5_hash",b"md5_hash",u"node_key",b"node_key",u"sha1_hash",b"sha1_hash",u"sha256_hash",b"sha256_hash",u"state",b"state"]) -> None: ...

class IpAddressDescription(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    node_key = ... # type: typing___Text
    timestamp = ... # type: builtin___int
    ip_address = ... # type: typing___Text
    ip_proto = ... # type: typing___Text

    def __init__(self,
        *,
        node_key : typing___Optional[typing___Text] = None,
        timestamp : typing___Optional[builtin___int] = None,
        ip_address : typing___Optional[typing___Text] = None,
        ip_proto : typing___Optional[typing___Text] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> IpAddressDescription: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"ip_address",u"ip_proto",u"node_key",u"timestamp"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[u"ip_address",b"ip_address",u"ip_proto",b"ip_proto",u"node_key",b"node_key",u"timestamp",b"timestamp"]) -> None: ...

class Session(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    primary_key_properties = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]
    primary_key_requires_asset_id = ... # type: builtin___bool
    created_time = ... # type: builtin___int
    last_seen_time = ... # type: builtin___int
    terminated_time = ... # type: builtin___int

    def __init__(self,
        *,
        primary_key_properties : typing___Optional[typing___Iterable[typing___Text]] = None,
        primary_key_requires_asset_id : typing___Optional[builtin___bool] = None,
        created_time : typing___Optional[builtin___int] = None,
        last_seen_time : typing___Optional[builtin___int] = None,
        terminated_time : typing___Optional[builtin___int] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> Session: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"created_time",u"last_seen_time",u"primary_key_properties",u"primary_key_requires_asset_id",u"terminated_time"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[u"created_time",b"created_time",u"last_seen_time",b"last_seen_time",u"primary_key_properties",b"primary_key_properties",u"primary_key_requires_asset_id",b"primary_key_requires_asset_id",u"terminated_time",b"terminated_time"]) -> None: ...

class Static(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    primary_key_properties = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]
    primary_key_requires_asset_id = ... # type: builtin___bool

    def __init__(self,
        *,
        primary_key_properties : typing___Optional[typing___Iterable[typing___Text]] = None,
        primary_key_requires_asset_id : typing___Optional[builtin___bool] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> Static: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"primary_key_properties",u"primary_key_requires_asset_id"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[u"primary_key_properties",b"primary_key_properties",u"primary_key_requires_asset_id",b"primary_key_requires_asset_id"]) -> None: ...

class IdStrategy(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def session(self) -> Session: ...

    @property
    def static(self) -> Static: ...

    def __init__(self,
        *,
        session : typing___Optional[Session] = None,
        static : typing___Optional[Static] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> IdStrategy: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"session",u"static",u"strategy"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"session",u"static",u"strategy"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"session",b"session",u"static",b"static",u"strategy",b"strategy"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"session",b"session",u"static",b"static",u"strategy",b"strategy"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions___Literal[u"strategy",b"strategy"]) -> typing_extensions___Literal["session","static"]: ...

class NodeProperty(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    intprop = ... # type: builtin___int
    uintprop = ... # type: builtin___int
    strprop = ... # type: typing___Text

    def __init__(self,
        *,
        intprop : typing___Optional[builtin___int] = None,
        uintprop : typing___Optional[builtin___int] = None,
        strprop : typing___Optional[typing___Text] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> NodeProperty: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"intprop",u"property",u"strprop",u"uintprop"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"intprop",u"property",u"strprop",u"uintprop"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"intprop",b"intprop",u"property",b"property",u"strprop",b"strprop",u"uintprop",b"uintprop"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"intprop",b"intprop",u"property",b"property",u"strprop",b"strprop",u"uintprop",b"uintprop"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions___Literal[u"property",b"property"]) -> typing_extensions___Literal["intprop","uintprop","strprop"]: ...

class DynamicNode(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class PropertiesEntry(google___protobuf___message___Message):
        DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
        key = ... # type: typing___Text

        @property
        def value(self) -> NodeProperty: ...

        def __init__(self,
            *,
            key : typing___Optional[typing___Text] = None,
            value : typing___Optional[NodeProperty] = None,
            ) -> None: ...
        @classmethod
        def FromString(cls, s: builtin___bytes) -> DynamicNode.PropertiesEntry: ...
        def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
        def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
        if sys.version_info >= (3,):
            def HasField(self, field_name: typing_extensions___Literal[u"value"]) -> builtin___bool: ...
            def ClearField(self, field_name: typing_extensions___Literal[u"key",u"value"]) -> None: ...
        else:
            def HasField(self, field_name: typing_extensions___Literal[u"value",b"value"]) -> builtin___bool: ...
            def ClearField(self, field_name: typing_extensions___Literal[u"key",b"key",u"value",b"value"]) -> None: ...

    node_key = ... # type: typing___Text
    node_type = ... # type: typing___Text
    seen_at = ... # type: builtin___int

    @property
    def properties(self) -> typing___MutableMapping[typing___Text, NodeProperty]: ...

    @property
    def asset_id(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    @property
    def hostname(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    @property
    def host_ip(self) -> google___protobuf___wrappers_pb2___StringValue: ...

    @property
    def id_strategy(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[IdStrategy]: ...

    def __init__(self,
        *,
        properties : typing___Optional[typing___Mapping[typing___Text, NodeProperty]] = None,
        node_key : typing___Optional[typing___Text] = None,
        node_type : typing___Optional[typing___Text] = None,
        seen_at : typing___Optional[builtin___int] = None,
        asset_id : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        hostname : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        host_ip : typing___Optional[google___protobuf___wrappers_pb2___StringValue] = None,
        id_strategy : typing___Optional[typing___Iterable[IdStrategy]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> DynamicNode: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def HasField(self, field_name: typing_extensions___Literal[u"asset_id",u"host_ip",u"hostname"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"asset_id",u"host_ip",u"hostname",u"id_strategy",u"node_key",u"node_type",u"properties",u"seen_at"]) -> None: ...
    else:
        def HasField(self, field_name: typing_extensions___Literal[u"asset_id",b"asset_id",u"host_ip",b"host_ip",u"hostname",b"hostname"]) -> builtin___bool: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"asset_id",b"asset_id",u"host_ip",b"host_ip",u"hostname",b"hostname",u"id_strategy",b"id_strategy",u"node_key",b"node_key",u"node_type",b"node_type",u"properties",b"properties",u"seen_at",b"seen_at"]) -> None: ...

class EdgeDescription(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    to = ... # type: typing___Text
    edgeName = ... # type: typing___Text

    def __init__(self,
        *,
        to : typing___Optional[typing___Text] = None,
        edgeName : typing___Optional[typing___Text] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> EdgeDescription: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"edgeName",u"from",u"to"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[u"edgeName",b"edgeName",u"from",b"from",u"to",b"to"]) -> None: ...

class EdgeList(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def edges(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[EdgeDescription]: ...

    def __init__(self,
        *,
        edges : typing___Optional[typing___Iterable[EdgeDescription]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> EdgeList: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"edges"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[u"edges",b"edges"]) -> None: ...

class GraphDescription(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class NodesEntry(google___protobuf___message___Message):
        DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
        key = ... # type: typing___Text

        @property
        def value(self) -> NodeDescription: ...

        def __init__(self,
            *,
            key : typing___Optional[typing___Text] = None,
            value : typing___Optional[NodeDescription] = None,
            ) -> None: ...
        @classmethod
        def FromString(cls, s: builtin___bytes) -> GraphDescription.NodesEntry: ...
        def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
        def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
        if sys.version_info >= (3,):
            def HasField(self, field_name: typing_extensions___Literal[u"value"]) -> builtin___bool: ...
            def ClearField(self, field_name: typing_extensions___Literal[u"key",u"value"]) -> None: ...
        else:
            def HasField(self, field_name: typing_extensions___Literal[u"value",b"value"]) -> builtin___bool: ...
            def ClearField(self, field_name: typing_extensions___Literal[u"key",b"key",u"value",b"value"]) -> None: ...

    class EdgesEntry(google___protobuf___message___Message):
        DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
        key = ... # type: typing___Text

        @property
        def value(self) -> EdgeList: ...

        def __init__(self,
            *,
            key : typing___Optional[typing___Text] = None,
            value : typing___Optional[EdgeList] = None,
            ) -> None: ...
        @classmethod
        def FromString(cls, s: builtin___bytes) -> GraphDescription.EdgesEntry: ...
        def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
        def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
        if sys.version_info >= (3,):
            def HasField(self, field_name: typing_extensions___Literal[u"value"]) -> builtin___bool: ...
            def ClearField(self, field_name: typing_extensions___Literal[u"key",u"value"]) -> None: ...
        else:
            def HasField(self, field_name: typing_extensions___Literal[u"value",b"value"]) -> builtin___bool: ...
            def ClearField(self, field_name: typing_extensions___Literal[u"key",b"key",u"value",b"value"]) -> None: ...

    timestamp = ... # type: builtin___int

    @property
    def nodes(self) -> typing___MutableMapping[typing___Text, NodeDescription]: ...

    @property
    def edges(self) -> typing___MutableMapping[typing___Text, EdgeList]: ...

    def __init__(self,
        *,
        nodes : typing___Optional[typing___Mapping[typing___Text, NodeDescription]] = None,
        edges : typing___Optional[typing___Mapping[typing___Text, EdgeList]] = None,
        timestamp : typing___Optional[builtin___int] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> GraphDescription: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"edges",u"nodes",u"timestamp"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[u"edges",b"edges",u"nodes",b"nodes",u"timestamp",b"timestamp"]) -> None: ...

class GeneratedSubgraphs(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def subgraphs(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[GraphDescription]: ...

    def __init__(self,
        *,
        subgraphs : typing___Optional[typing___Iterable[GraphDescription]] = None,
        ) -> None: ...
    @classmethod
    def FromString(cls, s: builtin___bytes) -> GeneratedSubgraphs: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    if sys.version_info >= (3,):
        def ClearField(self, field_name: typing_extensions___Literal[u"subgraphs"]) -> None: ...
    else:
        def ClearField(self, field_name: typing_extensions___Literal[u"subgraphs",b"subgraphs"]) -> None: ...
