FROM python:3.7.2-alpine

RUN pip install --upgrade setuptools wheel twine

COPY sdk /src/sdk

WORKDIR /src/sdk

RUN python setup.py sdist bdist_wheel

CMD python -m twine upload dist/*
