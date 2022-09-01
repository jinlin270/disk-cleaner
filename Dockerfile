FROM ubuntu:latest
ENV DEBIAN_FRONTEND=nonintercative
RUN apt-get update && apt-get install -y software-properties-common gcc && \
    add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python3.8 python3-distutils python3-pip python3-apt
RUN apt install wget
WORKDIR /disk_cleaner
COPY . /disk_cleaner
RUN python3 ./install.py

