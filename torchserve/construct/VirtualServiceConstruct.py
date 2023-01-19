#!/usr/bin/env python3
from constructs import Construct

from imports.io.istio import networking as nw


class VirtualServiceConstruct(Construct):

    def __init__(self, scope: Construct, *,
                namespace: str,
                gateway_name: str,
                app_name: str):
        id = "virtual-service"
        super().__init__(scope, id)

        spec_http = [
            nw.VirtualServiceSpecHttp(
                match=[nw.VirtualServiceSpecHttpMatch(uri=nw.VirtualServiceSpecHttpMatchUri(prefix="/pytorch/"))],
                rewrite=nw.VirtualServiceSpecHttpRewrite(uri="/"),
                route=[
                    nw.VirtualServiceSpecHttpRoute(
                        destination=nw.VirtualServiceSpecHttpRouteDestination(
                            host=app_name,
                            port=nw.VirtualServiceSpecHttpRouteDestinationPort(number=8080)
                        )
                    )
                ]
            )
        ]

        nw.VirtualService(
            self, id,
            metadata={"name": "modelserve-inference-vs", "namespace": namespace},
            spec=nw.VirtualServiceSpec(
                hosts=["*"],
                gateways=[gateway_name],
                http=spec_http
            )
        )