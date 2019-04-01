FROM ubuntu:xenial

ARG HOST_UID
ARG HOST_GID
RUN groupadd -r sdkuser && useradd -r -u $HOST_UID -g sdkuser sdkuser

RUN apt-get update && \
    apt-get -y install \
        git \
        vim \
        telnet \
        make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
        libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev \
        software-properties-common pandoc

RUN add-apt-repository -y ppa:ethereum/ethereum && \
    apt-get update && \
    apt-get -y install solc ethereum

COPY Docker/sdk/entrypoint.sh /usr/local/bin/entrypoint.sh

# grab gosu for easy step-down from root (https://github.com/tianon/gosu/releases)
ENV GOSU_VERSION 1.10

RUN dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
	  wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
	  wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
	  export GNUPGHOME="$(mktemp -d)"; \
	  gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \
	  gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
	  command -v gpgconf && gpgconf --kill all || :; \
	  rm -r "$GNUPGHOME" /usr/local/bin/gosu.asc; \
	  chmod +x /usr/local/bin/gosu; \
	  gosu nobody true; \
	  chmod +x /usr/local/bin/entrypoint.sh

ENV PYENV_ROOT /home/sdkuser/.pyenv
RUN curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash && \
    /home/sdkuser/.pyenv/bin/pyenv install 3.7.2

COPY sdk/requirements.txt /home/sdkuser/sdk/requirements.txt

WORKDIR /home/sdkuser/sdk

ENV PATH="/home/sdkuser/.pyenv/versions/3.7.2/bin:${PATH}"

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONPATH /home/sdkuser/sdk

RUN pip install -r requirements.txt && \
    git clone https://github.com/unification-com/wrkchain-root-contract.git --depth 1

COPY sdk /home/sdkuser/sdk
COPY templates /home/sdkuser/templates

RUN echo "py.test /home/sdkuser/src/tests" >> /home/sdkuser/.bash_history && \
    echo "python -m wrkchain.sdk generate_wrkchain /home/sdkuser/wrkchain.json /home/sdkuser/build" >> /home/sdkuser/.bash_history && \
    echo "py.test /home/sdkuser/sdk/systemtests" >> /home/sdkuser/.bash_history && \
    echo "alias ll='ls -la'" >> /home/sdkuser/.bashrc

RUN chown -R sdkuser /home/sdkuser

COPY wrkchain.json /home/sdkuser/wrkchain.json

RUN py.test /home/sdkuser/sdk/tests

ENV HOST_BUILD_DIR=""

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["python", "-m", "wrkchain.sdk", "generate_wrkchain", "/home/sdkuser/wrkchain.json", "/home/sdkuser/build", "--host_build_dir=${HOST_BUILD_DIR}"]
