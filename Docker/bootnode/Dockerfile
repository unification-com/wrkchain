FROM ubuntu:xenial

RUN apt-get update \
     && apt-get install -y wget software-properties-common \
     && rm -rf /var/lib/apt/lists/*

WORKDIR "/root"

RUN add-apt-repository -y ppa:ethereum/ethereum

RUN apt-get update \
     && apt-get install -y ethereum

COPY build/bootnode.key /root/assets/bootnode.key

ARG BOOTNODE_PORT
CMD exec bootnode -nodekey /root/assets/bootnode.key -verbosity 4 --addr :$BOOTNODE_PORT

EXPOSE $BOOTNODE_PORT
