#!/usr/bin/env python3
from constructs import Construct

from imports import k8s

class ServiceConstruct(Construct):

    def __init__(self, scope: Construct, *, metadata: k8s.ObjectMeta, label: dict):
        super().__init__(scope, "service")
        
        ports = [
            k8s.ServicePort(name="preds", port=8080, target_port=k8s.IntOrString.from_string("ts")),
            k8s.ServicePort(name="mdl", port=8081, target_port=k8s.IntOrString.from_string("ts-management")),
            k8s.ServicePort(name="metrics", port=8082, target_port=k8s.IntOrString.from_string("ts-metrics"))
        ]

        k8s.KubeService(
            self, "service",
            metadata=metadata,
            spec=k8s.ServiceSpec(
                type="LoadBalancer",
                selector=label,
                ports=ports
            )
        )