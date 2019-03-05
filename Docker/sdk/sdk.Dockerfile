FROM debian:stretch-slim

RUN apt-get update && \
    apt-get -y install \
        git \
        vim \
        telnet \
        make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
        libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev

RUN curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash && \
    /root/.pyenv/bin/pyenv install 3.7.1

RUN mkdir /src
COPY sdk/requirements.txt /src/requirements.txt

WORKDIR /src

ENV PATH="/root/.pyenv/versions/3.7.1/bin:${PATH}"

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONPATH /src

RUN pip install -r requirements.txt

RUN echo "py.test /src/tests" >> /root/.bash_history && \
    echo "python -m workchain_sdk.config validate /examples/config.json" >> /root/.bash_history && \
    echo "alias ll='ls -la'" >> /root/.bashrc

COPY sdk/workchain_sdk /src/workchain_sdk
COPY sdk/tests /src/tests
COPY examples /examples

CMD ["py.test", "/src/tests"]
