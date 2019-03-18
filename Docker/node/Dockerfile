FROM ubuntu:xenial

RUN apt-get update \
     && apt-get install -y wget software-properties-common \
     && rm -rf /var/lib/apt/lists/*

WORKDIR "/root"

RUN add-apt-repository -y ppa:ethereum/ethereum

ARG binary
RUN apt-get update \
     && apt-get install -y ethereum

ARG WALLET_PASS
ARG PRIVATE_KEY
ARG GENESIS_JSON_FILENAME
RUN echo $WALLET_PASS > /root/.walletpassword
RUN echo $PRIVATE_KEY > /root/.privatekey
ADD ./assets/build/$GENESIS_JSON_FILENAME /root/assets/genesis.json
RUN geth init /root/assets/genesis.json
RUN geth account import --password /root/.walletpassword  /root/.privatekey

ENV BOOTNODE_ID=""
ENV BOOTNODE_IP=""
ENV BOOTNODE_PORT=""
ENV WRKCHAIN_NETWORK_ID=""
ENV GETH_LISTEN_PORT=""
ENV RPC_PORT=""

CMD exec geth --bootnodes "enode://$BOOTNODE_ID@$BOOTNODE_IP:$BOOTNODE_PORT" --networkid "$WRKCHAIN_NETWORK_ID" --verbosity=4 --rpc --rpcaddr "0.0.0.0" --rpcport "$RPC_PORT" --rpcapi "eth,web3,net,admin,debug,db" --rpccorsdomain "*" --syncmode="full" --port $GETH_LISTEN_PORT

EXPOSE $RPC_PORT
EXPOSE $GETH_LISTEN_PORT