#!/usr/bin/env python3
from constructs import Construct

from imports import k8s

class NamespaceConstruct(Construct):

    def __init__(self, scope: Construct, *, 
                name: str,
                useIstio: bool):
        super().__init__(scope, "namespace")

        labels = {"istio-injection": "enabled"} if useIstio is True else {}
        k8s.KubeNamespace(self, name, metadata=k8s.ObjectMeta(name=name, labels=labels))
