#!/usr/bin/env python3
from constructs import Construct

from imports import k8s

from construct.RequestAuthenticationConstruct import RequestAuthenticationConstruct 
from construct.AuthorizationPolicyConstruct import AuthorizationPolicyConstruct
from construct.GatewayConstruct import GatewayConstruct
from construct.VirtualServiceConstruct import VirtualServiceConstruct

class IstioService(Construct):

    def __init__(self, scope: Construct, id: str, *, namespace: str, app_name: str):
        super().__init__(scope, id)

        self.namespace = namespace
        self.app_name = app_name

        self.createRequestAuthentication()
        self.createAuthorizationPolicy()
        self.createGateway()

    
    def createRequestAuthentication(self):
        RequestAuthenticationConstruct(self, namespace=self.namespace, app_name=self.app_name)

    def createAuthorizationPolicy(self):
        AuthorizationPolicyConstruct(self, namespace=self.namespace, app_name=self.app_name, action="ALLOW", rules_values=["inference:pytorch"])

    def createGateway(self):
        gateway_name = "modelserve-gateway"
        GatewayConstruct(self, namespace=self.namespace, gateway_name=gateway_name, port=80)
        VirtualServiceConstruct(self, namespace=self.namespace, gateway_name=gateway_name, app_name=self.app_name)
