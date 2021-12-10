FROM python:3.9-slim

RUN apt-get update && apt-get install -y wget unzip && \
    pip install awscli && \
    wget https://releases.hashicorp.com/terraform/1.1.0/terraform_1.1.0_linux_amd64.zip && \
    unzip terraform_1.1.0_linux_amd64.zip && \
    mv terraform /usr/bin/terraform