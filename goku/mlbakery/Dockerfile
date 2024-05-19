# Use an appropriate base image
FROM ubuntu:latest

# Install necessary packages
RUN apt-get update && \
    apt-get install -y g++

RUN apt-get install -y python3 python3-pip git htop

# Ensure /bin/sh is available
RUN if [ ! -e /bin/sh ]; then ln -s /bin/bash /bin/sh; fi

# Copy the model file into the container
COPY . /model/