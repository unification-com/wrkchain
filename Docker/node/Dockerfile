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

RUN wget https://dl.google.com/go/go1.$GO_VERSION.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.$GO_VERSION.linux-amd64.tar.gz && \
    rm go1.$GO_VERSION.linux-amd64.tar.gz && \
    mkdir ~/.go

ENV GOPATH="/root/.go"
ENV GOROOT="/usr/local/go"
ENV PATH="/usr/local/go/bin:${PATH}"

RUN go get github.com/ethereum/go-ethereum
RUN go install github.com/ethereum/go-ethereum/cmd/geth

ARG WALLET_PASS
ARG PRIVATE_KEY

ADD build/genesis.json /root/assets/genesis.json
COPY build/node_keys /root/node_keys
COPY build/static-nodes-docker.json /root/.ethereum/static-nodes.json

RUN echo $WALLET_PASS > /root/.walletpassword
RUN echo $PRIVATE_KEY > /root/.privatekey
RUN /root/.go/bin/geth init /root/assets/genesis.json
RUN /root/.go/bin/geth account import --password /root/.walletpassword  /root/.privatekey
