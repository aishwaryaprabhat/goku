# Use an appropriate base image
FROM ubuntu:latest

# Install necessary packages
RUN apt-get update && \
    apt-get install -y g++

# Copy the model file into the container
COPY . /model/
