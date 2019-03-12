FROM python:3.7.2-alpine

RUN pip install --upgrade --index-url https://pypi.org/simple/ workchain

CMD python -i -m workchain.config
