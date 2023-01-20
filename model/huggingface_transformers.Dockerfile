FROM lindseynoh3/torcharchiver:latest

ARG now
ARG version

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

# 구성 환경에 맞게 아래 정보가 필요합니다.
# GCS 버킷명
ENV bucket_name=
# gcloud service account
ENV service_account_file=
# Auth0 토큰 : authorization: Bearer 을 앞에 붙여 입력하세요
ENV token=
# {torchserve service/torchserve IP}:8081
ENV torchserve_url=

# 학습 모델 mar 파일 Cloud Storage에 업로드
ENV filename=BERTSeqClassification_$now.mar
RUN echo $filename
RUN mv BERTSeqClassification.mar $filename
COPY $service_account_file /serve 
RUN gcloud auth activate-service-account --key-file /serve/${service_account_file}
RUN gcloud config set project supertone
RUN gcloud storage cp ${filename} gs://${bucket_name}/

# torchserve 모델 등록
ENV register_url=${torchserve_url}/models?model_name=BERTSeqClassification&url=https://storage.googleapis.com/${bucket_name}/${filename}&batch_size=4&max_batch_delay=5000&initial_workers=1&synchronous=true
RUN echo $register_url
RUN echo $token
RUN curl -X POST $register_url --header "$token"

# torchserve default version 변경
ENV update_version_url=${torchserve_url}/models/BERTSeqClassification/${version}/set-default
RUN echo $update_version_url
RUN curl -v -X PUT $register_url --header "$token"