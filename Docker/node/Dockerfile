FROM debian:stretch-slim

RUN apt-get update && \
    apt-get -y install \
        build-essential \
        git \
        telnet \
        vim \
        wget

WORKDIR "/root"

ARG GO_VERSION
ARG PRIVATE_KEY
ARG WALLET_PASS
ARG WRKCHAIN_DATA_DIR

RUN wget https://dl.google.com/go/go1.$GO_VERSION.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.$GO_VERSION.linux-amd64.tar.gz && \
    rm go1.$GO_VERSION.linux-amd64.tar.gz && \
    mkdir ~/.go

ENV GOPATH="/root/.go"
ENV GOROOT="/usr/local/go"
ENV PATH="/usr/local/go/bin:${PATH}"

RUN go get github.com/ethereum/go-ethereum
RUN go install github.com/ethereum/go-ethereum/cmd/geth

ADD build/genesis.json /root/$WRKCHAIN_DATA_DIR/genesis.json
COPY build/node_keys /root/$WRKCHAIN_DATA_DIR/node_keys
COPY build/static-nodes-docker.json /root/$WRKCHAIN_DATA_DIR/static-nodes.json

RUN echo $WALLET_PASS > /root/.walletpassword
RUN echo $PRIVATE_KEY > /root/.privatekey
RUN /root/.go/bin/geth --datadir=/root/$WRKCHAIN_DATA_DIR init /root/$WRKCHAIN_DATA_DIR/genesis.json
RUN /root/.go/bin/geth --datadir=/root/$WRKCHAIN_DATA_DIR account import --password /root/.walletpassword  /root/.privatekey
