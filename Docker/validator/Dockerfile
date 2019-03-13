FROM ubuntu:xenial

RUN apt-get update \
     && apt-get install -y wget software-properties-common \
     && rm -rf /var/lib/apt/lists/*

WORKDIR "/root"

RUN add-apt-repository -y ppa:ethereum/ethereum

RUN apt-get update \
     && apt-get install -y ethereum

ARG WALLET_PASS
ARG PRIVATE_KEY
ARG GETH_LISTEN_PORT

ADD build/genesis.json /root/assets/genesis.json
COPY build/node_keys /root/node_keys
COPY build/static-nodes.json /root/static-nodes.json

RUN echo $WALLET_PASS > /root/.walletpassword
RUN echo $PRIVATE_KEY > /root/.privatekey
RUN geth init /root/assets/genesis.json
RUN geth account import --password /root/.walletpassword  /root/.privatekey

EXPOSE $GETH_LISTEN_PORT
