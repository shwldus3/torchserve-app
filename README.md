#### Import istio crd
	cdk8s import crds/istio_crds.yaml

#### Generate k8s manifests in "dist/"
	cdk8s synth

#### Deploy
   kubectl apply -f dist/