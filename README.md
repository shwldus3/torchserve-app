#### Import istio crd
	cdk8s import crds/istio_crds.yaml

#### Generate k8s manifests in "dist/"
	cdk8s synth

#### Deploy
  kubectl apply -f dist/

#### Register sample model
  ```bash
    docker build -f HuggingfaceTransformers.Dockerfile \
    --build-arg now="$(date +%G%m%d_%H%M%S)" \
    --build-arg version=1.0 \
    .
  ```

#### Test
  ```
    curl -X POST http://{ingressgateway IP}/pytorch/predictions/BERTSeqClassification \
    -T samples/sample_text_captum_input.txt \
    --header 'authorization: Bearer {token}'
  ``` 