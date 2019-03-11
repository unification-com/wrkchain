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
ARG GENESIS_JSON_FILENAME
ARG GETH_LISTEN_PORT

RUN echo $WALLET_PASS > /root/.walletpassword
RUN echo $PRIVATE_KEY > /root/.privatekey
ADD build/$GENESIS_JSON_FILENAME /root/assets/genesis.json
RUN geth init /root/assets/genesis.json
RUN geth account import --password /root/.walletpassword  /root/.privatekey

EXPOSE $GETH_LISTEN_PORT
