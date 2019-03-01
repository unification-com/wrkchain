FROM ubuntu:xenial

RUN apt-get update && \
    apt-get -y install \
        git \
        vim \
        telnet \
        make build-essential software-properties-common \
        wget curl && \
    apt-get autoremove && \
    apt-get clean

WORKDIR "/root"

RUN wget https://dl.google.com/go/go1.10.3.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.10.3.linux-amd64.tar.gz && \
    mkdir ~/.go

ENV GOPATH="/root/.go"
ENV GOROOT="/usr/local/go"

RUN mkdir /root/.ssh && \
    mkdir -p ${GOPATH}/src/github.com/unification-com && \
    cd ${GOPATH}/src/github.com/unification-com && \
    git clone https://github.com/unification-com/mainchain.git && \
    git clone https://github.com/unification-com/oracle

ENV PATH="/usr/local/go/bin:/root/.go/bin:${PATH}"

ENV MAINCHAIN_WEB3_PROVIDER_URL=""
ENV WORKCHAIN_WEB3_PROVIDER_URL=""
ENV PRIVATE_KEY=""
ENV WORKCHAIN_ROOT_CONTRACT_ADDRESS=""
ENV WORKCHAIN_ROOT_WRITE_TIMEOUT=""
ENV WORKCHAIN_NETWORK_ID=""

RUN echo "go run /root/.go/src/github.com/unification-com/oracle/oracle.go" >> /root/.bash_history && \
    echo "alias ll='ls -la'" >> /root/.bashrc

CMD go run /root/.go/src/github.com/unification-com/oracle/oracle.go "$WORKCHAIN_WEB3_PROVIDER_URL" "$MAINCHAIN_WEB3_PROVIDER_URL" "$PRIVATE_KEY" "$WORKCHAIN_ROOT_CONTRACT_ADDRESS" $WORKCHAIN_ROOT_WRITE_TIMEOUT $WORKCHAIN_NETWORK_ID 2>&1 | tee /root/oracle_log.txt
