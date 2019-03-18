FROM python:3.7.2

RUN apt-get install -y gcc

RUN pip install --upgrade --index-url https://pypi.org/simple/ workchain

COPY examples /examples

CMD python -m wrkchain.sdk generate-wrkchain /examples/config.json /build
