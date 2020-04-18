#
# The One True Grapl Rust Dockerfile
#
# This file is where we build and create all our Rust images. This
# is to avoid having to build the project dependencies multiple times
# (e.g. once for each individual binary). Instead, we build all the
# Rust code once and then pull out all the binaries into their own
# images.
#

# grapl/grapl_rust_base sets USER rust
FROM grapl/grapl_rust_base AS grapl-rust-build
RUN mkdir -p /home/rust/grapl
WORKDIR /home/rust/grapl
COPY --chown=rust . .
# TODO cargo clean && cargo test && cargo build --release once tests work
RUN cargo build --release

# analyzer-dispatcher
FROM alpine AS grapl-analyzer-dispatcher
COPY --from=grapl-rust-build /home/rust/grapl/target/x86_64-unknown-linux-musl/release/analyzer-dispatcher /

# graph-merger
FROM alpine AS grapl-graph-merger
COPY --from=grapl-rust-build /home/rust/grapl/target/x86_64-unknown-linux-musl/release/graph-merger /

# node-identifier
FROM alpine AS grapl-node-identifier
COPY --from=grapl-rust-build /home/rust/grapl/target/x86_64-unknown-linux-musl/release/node-identifier /
COPY --from=grapl-rust-build /home/rust/grapl/target/x86_64-unknown-linux-musl/release/node-identifier-retry-handler /

# sysmon-subgraph-generator
FROM alpine AS grapl-sysmon-subgraph-generator
COPY --from=grapl-rust-build /home/rust/grapl/target/x86_64-unknown-linux-musl/release/sysmon-subgraph-generator /