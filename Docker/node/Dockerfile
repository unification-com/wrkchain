FROM debian:stretch-slim

RUN apt-get update && \
    apt-get -y install \
        build-essential \
        git \
        telnet \
        vim \
        wget

WORKDIR "/root"

RUN wget https://dl.google.com/go/go1.10.3.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.10.3.linux-amd64.tar.gz && \
    mkdir ~/.go

ENV GOPATH="/root/.go"
ENV GOROOT="/usr/local/go"
ENV PATH="/usr/local/go/bin:${PATH}"

RUN go get github.com/ethereum/go-ethereum
RUN go install github.com/ethereum/go-ethereum/cmd/geth

ARG binary

ARG WALLET_PASS
ARG PRIVATE_KEY
ARG GENESIS_JSON_FILENAME
RUN echo $WALLET_PASS > /root/.walletpassword
RUN echo $PRIVATE_KEY > /root/.privatekey
ADD ./assets/build/$GENESIS_JSON_FILENAME /root/assets/genesis.json
RUN /root/.go/bin/geth init /root/assets/genesis.json
RUN /root/.go/bin/geth account import --password /root/.walletpassword  /root/.privatekey

ENV BOOTNODE_ID=""
ENV BOOTNODE_IP=""
ENV BOOTNODE_PORT=""
ENV WRKCHAIN_NETWORK_ID=""
ENV GETH_LISTEN_PORT=""
ENV RPC_PORT=""

CMD exec /root/.go/bin/geth --bootnodes "enode://$BOOTNODE_ID@$BOOTNODE_IP:$BOOTNODE_PORT" --networkid "$WRKCHAIN_NETWORK_ID" --verbosity=4 --rpc --rpcaddr "0.0.0.0" --rpcport "$RPC_PORT" --rpcapi "eth,web3,net,admin,debug,db" --rpccorsdomain "*" --syncmode="full" --port $GETH_LISTEN_PORT

EXPOSE $RPC_PORT
EXPOSE $GETH_LISTEN_PORT
