FROM ubuntu:xenial

RUN apt-get update && \
    apt-get -y install \
        git \
        vim \
        telnet \
        make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
        libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev \
        software-properties-common

RUN add-apt-repository -y ppa:ethereum/ethereum && \
    apt-get update && \
    apt-get -y install solc ethereum pandoc

RUN curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash && \
    /root/.pyenv/bin/pyenv install 3.7.2

RUN mkdir /src
COPY sdk/requirements.txt /src/requirements.txt

WORKDIR /src

ENV PATH="/root/.pyenv/versions/3.7.2/bin:${PATH}"

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONPATH /src/sdk

RUN pip install -r requirements.txt && \
    git clone https://github.com/unification-com/workchain-root-contract.git --depth 1

RUN echo "py.test /src/sdk/tests" >> /root/.bash_history && \
    echo "python -m workchain.sdk generate_workchain /examples/config.json /build" >> /root/.bash_history && \
    echo "py.test /src/sdk/systemtests" >> /root/.bash_history && \
    echo "alias ll='ls -la'" >> /root/.bashrc

COPY sdk /src/sdk

COPY sdk/tests/test_data /examples

RUN py.test /src/sdk/tests

CMD ["python", "-m", "workchain.sdk", "generate_workchain", "/examples/config.json", "/build"]
