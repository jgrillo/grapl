#
# The One True Grapl Rust Dockerfile
#
# This file is where we build and create all our Rust images. This
# is to avoid having to build the project dependencies multiple times
# (e.g. once for each individual binary). Instead, we build all the
# Rust code once and then pull out all the binaries into their own
# images. Additionally, we leverage cargo vendor and docker's cache
# to minimize the amount of compilation required during local builds.
#
# See:
#  https://benjamincongdon.me/blog/2019/12/04/Fast-Rust-Docker-Builds-with-cargo-vendor/
#  https://github.com/rust-lang/cargo/issues/2644
#

FROM rust:alpine AS grapl-rust-build
ARG release_target="release"
RUN apk add --no-cache musl-dev
RUN adduser -D --gecos '' --home /home/grapl --shell /bin/bash grapl
USER grapl
ENV USER grapl
RUN mkdir /home/grapl/grapl
WORKDIR /home/grapl/grapl
# build a fake project structure, but copy in the real Cargo.tomls
RUN cargo new --bin analyzer-dispatcher
COPY --chown=grapl analyzer-dispatcher/Cargo.toml analyzer-dispatcher/Cargo.toml
RUN cargo new --lib derive-dynamic-node
COPY --chown=grapl derive-dynamic-node/Cargo.toml derive-dynamic-node/Cargo.toml
RUN cargo new --bin generic-subgraph-generator
COPY --chown=grapl generic-subgraph-generator/Cargo.toml generic-subgraph-generator/Cargo.toml
RUN cargo new --lib graph-descriptions
COPY --chown=grapl graph-descriptions/Cargo.toml graph-descriptions/Cargo.toml
RUN cargo new --lib graph-generator-lib
COPY --chown=grapl graph-generator-lib/Cargo.toml graph-generator-lib/Cargo.toml
RUN cargo new --bin graph-merger
COPY --chown=grapl graph-merger/Cargo.toml graph-merger/Cargo.toml
RUN cargo new --lib grapl-config
COPY --chown=grapl grapl-config/Cargo.toml grapl-config/Cargo.toml
# this is gross, we have to do it because node-identifier's Cargo.toml as [[bin]] sections
RUN cargo new --bin node-identifier && \
  mkdir -p node-identifier/src/bin && \
  cp node-identifier/src/main.rs node-identifier/src/bin/node-identifier.rs && \
  cp node-identifier/src/main.rs node-identifier/src/bin/node-identifier-retry-handler.rs
COPY --chown=grapl node-identifier/Cargo.toml node-identifier/Cargo.toml
RUN cargo new --bin sysmon-subgraph-generator
COPY --chown=grapl sysmon-subgraph-generator/Cargo.toml sysmon-subgraph-generator/Cargo.toml
# copy in the top-level Cargo.toml and Cargo.lock
COPY --chown=grapl Cargo.lock .
COPY --chown=grapl Cargo.toml .
# vendor and build the deps
RUN mkdir /home/grapl/grapl/.cargo
RUN cargo vendor > /home/grapl/grapl/.cargo/config
# FIXME: cargo test instead of cargo build once the tests work
RUN RUSTFLAGS="-C target-feature=-crt-static" cargo build
RUN RUSTFLAGS="-C target-feature=-crt-static" cargo build --release
# remove all the fake project crap
RUN rm -r analyzer-dispatcher && \
  rm -r derive-dynamic-node && \
  rm -r generic-subgraph-generator && \
  rm -r graph-descriptions && \
  rm -r graph-generator-lib && \
  rm -r graph-merger && \
  rm -r grapl-config
# copy in the source tree (we do this part separately s.t. docker caches the deps)
COPY --chown=grapl ./ .
# build everything
# FIXME: cargo test instead of cargo build once the tests work
RUN RUSTFLAGS="-C target-feature=-crt-static" cargo build
RUN RUSTFLAGS="-C target-feature=-crt-static" cargo build --release
RUN mkdir -p ~/bin/${release_target}
RUN cp target/${release_target}/analyzer-dispatcher ~/bin/${release_target}/ && \
    cp target/${release_target}/graph-merger ~/bin/${release_target}/ && \
    cp target/${release_target}/node-identifier ~/bin/${release_target}/ && \
    cp target/${release_target}/node-identifier-retry-handler ~/bin/${release_target}/ && \
    cp target/${release_target}/sysmon-subgraph-generator ~/bin/${release_target}/
# analyzer-dispatcher
FROM alpine AS grapl-analyzer-dispatcher
COPY --from=grapl-rust-build /home/grapl/bin/${release_target}/analyzer-dispatcher /
CMD ["analyzer-dispatcher"]

# graph-merger
FROM alpine AS grapl-graph-merger
COPY --from=grapl-rust-build /home/grapl/bin/${release_target}/graph-merger /
CMD ["graph-merger"]

# node-identifier
FROM alpine AS grapl-node-identifier
COPY --from=grapl-rust-build /home/grapl/bin/${release_target}/node-identifier /
CMD ["node-identifier"]

FROM alpine AS grapl-node-identifier-retry-handler
COPY --from=grapl-rust-build /home/grapl/bin/${release_target}/node-identifier-retry-handler /
CMD ["node-identifier-retry-handler"]

# sysmon-subgraph-generator
FROM alpine AS grapl-sysmon-subgraph-generator
COPY --from=grapl-rust-build /home/grapl/bin/${release_target}/sysmon-subgraph-generator /
CMD ["sysmon-subgraph-generator"]
