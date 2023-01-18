# Prerequisite
- [Docker](https://docs.docker.com/get-docker/)
- [Google GKE Cluster](https://github.com/pytorch/serve/blob/master/kubernetes/README.md#-Torchserve-on-Kubernetes)
- [Istio](https://istio.io/latest/docs/setup/getting-started/)
- [Auth0](https://auth0.com/)
- [cdk8s](https://cdk8s.io/docs/latest/getting-started/)

# How to use
## Deploy pytorch/serve 
#### 1. Move to model directory
  ```bash
    cd torchserve
  ```

#### 2. Import istio crd
  ```bash
	  cdk8s import crds/istio_crds.yaml
  ```

#### 3. Generate k8s manifests in "dist/"
  ```bash
    cdk8s synth
  ```

#### 4. Deploy
  ```bash
    kubectl apply -f dist/
  ```

## Serving model with pytorch/serve 
#### 1. Move to model directory
  ```bash
    cd model
  ```

#### 2. Register sample model
  ```bash
    docker build -f HuggingfaceTransformers.Dockerfile \
    --build-arg now="$(date +%G%m%d_%H%M%S)" \
    --build-arg version=1.0 \
    .
  ```

#### 3. Test
  ```
    curl -X POST http://{ingressgateway IP}/pytorch/predictions/BERTSeqClassification \
    -T samples/sample_text_captum_input.txt \
    --header 'authorization: Bearer {token}'
  ``` 