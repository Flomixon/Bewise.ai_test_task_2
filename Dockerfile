FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip

RUN yes | apt-get install ffmpeg

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY ./ /app

WORKDIR /app
