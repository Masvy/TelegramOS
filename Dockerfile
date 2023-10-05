FROM python:3.10-alpine

RUN mkdir /src
WORKDIR /src

ADD ./tgbot .
ADD ./requirements.txt .

RUN pip install -r ./requirements.txt