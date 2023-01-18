#!/usr/bin/env python3
from constructs import Construct

from imports.io.istio import networking as nw


class GatewayConstruct(Construct):

    def __init__(self, scope: Construct, *,
                namespace: str,
                gateway_name: str):
        id = "Gateway"
        super().__init__(scope, id)

        labels = {"app": gateway_name}
        gateway_servers = [
            nw.GatewaySpecServers(
                port=nw.GatewaySpecServersPort(number=80, name="http", protocol="HTTP"),
                hosts=["*"]
            )
        ]

        nw.Gateway(self, id,
            metadata={"name": gateway_name, "namespace": namespace, "labels": labels},
            spec=nw.GatewaySpec(
                selector={"istio": "ingressgateway"},
                servers=gateway_servers
            )
        )