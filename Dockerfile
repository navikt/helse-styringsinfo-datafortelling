FROM navikt/python:3.11

USER root
RUN python -m pip install --upgrade pip wheel

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY main.py .