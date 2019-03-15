FROM python:3.7.2

RUN apt-get update && \
    apt-get install -y gcc pandoc

RUN pip install --upgrade --index-url https://pypi.org/simple/ workchain

COPY sdk/tests/test_data/config.json /examples/config.json

CMD python -m workchain.sdk generate-workchain /examples/config.json /build
