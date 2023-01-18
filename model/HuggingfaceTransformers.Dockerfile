FROM ubuntu:18.04

ARG now
ARG version

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

# 작업위치 변경
WORKDIR serve/examples/Huggingface_Transformers

# Text Generation을 위한 config파일 적용
COPY setup_config.json ./ 

# 학습 모델 다운로드
RUN mkdir Transformer_model
RUN python3 Download_Transformer_models.py

# torchserve를 위한 mar파일 생성
RUN echo $version
RUN torch-model-archiver --model-name BERTSeqClassification --version $version --serialized-file Transformer_model/pytorch_model.bin --handler ./Transformer_handler_generalized.py --extra-files "Transformer_model/config.json,./setup_config.json,./Seq_classification_artifacts/index_to_name.json"

# 환경에 맞게 아래의 bucket_name, gcloud service account, torchserve LB 정보는 변경해야 합니다.
ENV bucket_name=test-model-storage
ENV service_account_path=supertone-374908-199d4c154d6c.json
ENV torchserve_url=34.146.41.134:8081

# 학습 모델 mar 파일 Cloud Storage에 업로드
ENV filename=BERTSeqClassification_$now.mar
RUN echo $filename
RUN mv BERTSeqClassification.mar $filename
COPY $service_account_path /serve 
RUN gcloud auth activate-service-account --key-file /serve/supertone-374908-199d4c154d6c.json
RUN gcloud config set project supertone
RUN gcloud storage cp ${filename} gs://${bucket_name}/

# torchserve 모델 등록
ENV torchserve_url=${torchserve_url}/models?model_name=BERTSeqClassification&url=https://storage.cloud.google.com/${bucket_name}/${filename}&batch_size=4&max_batch_delay=5000&initial_workers=3&synchronous=true
RUN echo $torchserve_url
RUN curl -X POST $torchserve_url