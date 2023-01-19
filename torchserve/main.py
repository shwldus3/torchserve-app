#!/usr/bin/env python3
from constructs import Construct
from cdk8s import App, Chart

from service.TorchserveService import TorchserveService
from service.IstioService import IstioService


class TorchserveChart(Chart):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        namespace = "modelserve"
        app_name="torchserve"
        
        TorchserveService(self, app_name, namespace=namespace) 
        IstioService(self, app_name=app_name, namespace=namespace) 


app = App()        
TorchserveChart(app, "torchserve-app")
app.synth()
