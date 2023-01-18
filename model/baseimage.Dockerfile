FROM ubuntu:18.04

# Python, pip, git, curl, gcloud 설치
RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip
RUN apt-get install -y git
RUN apt-get -y install curl
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-cli -y

# pip package 설치
RUN pip3 install transformers==4.6.0
RUN pip3 install torch torch-model-archiver

# torchserve 소스코드 다운로드
RUN git clone https://github.com/pytorch/serve.git
RUN cd serve/model-archiver && pip3 install .