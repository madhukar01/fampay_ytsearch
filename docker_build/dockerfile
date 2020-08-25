# Use ubuntu 20.04 LTS image
FROM ubuntu:20.04

# Copy current directory files to /app
COPY . /app
# Set Working directory to /app
WORKDIR /app

# Install python3
RUN apt-get update &&\
    apt-get install -y python3-dev python3-pip

# Install dependencies
RUN pip3 install -r requirements.txt
