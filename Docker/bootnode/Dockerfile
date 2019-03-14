FROM ubuntu:xenial

RUN apt-get update \
     && apt-get install -y wget software-properties-common \
     && rm -rf /var/lib/apt/lists/*

WORKDIR "/root"

RUN add-apt-repository -y ppa:ethereum/ethereum

RUN apt-get update \
     && apt-get install -y ethereum

COPY build/node_keys /root/node_keys

ARG BOOTNODE_PORT
CMD exec bootnode -nodekey /root/node_keys/bootnode.key -verbosity 4 --addr :$BOOTNODE_PORT

EXPOSE $BOOTNODE_PORT
