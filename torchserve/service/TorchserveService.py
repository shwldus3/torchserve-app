#!/usr/bin/env python3
from constructs import Construct

from imports import k8s

from construct.PvcConstruct import PvcConstruct
from construct.ServiceConstruct import ServiceConstruct 
from construct.DeploymentConstruct import DeploymentConstruct 
from construct.NamespaceConstruct import NamespaceConstruct 

class TorchserveService(Construct):

    def __init__(self, scope: Construct, id: str, *, namespace: str):
        super().__init__(scope, id)

        self.name = id
        self.namespace = namespace
        self.pvc_name = "model-store-claim"
        self.label = {"app": id}
        self.metadata = k8s.ObjectMeta(name=id, namespace=namespace, labels=self.label)

        self.createNamespace()
        self.createPvc()
        self.createService()
        self.createDeployment()


    def createNamespace(self):
        NamespaceConstruct(self, name=self.namespace, useIstio=True)

    
    def createService(self):
        ServiceConstruct(self, metadata=self.metadata, label=self.label)


    def createDeployment(self):
        DeploymentConstruct(self,
                            name=self.name,
                            metadata=self.metadata, 
                            label=self.label, 
                            image="pytorch/torchserve:latest",
                            pvc_name=self.pvc_name, 
                            volume_mount_name="persistent-storage")


    def createPvc(self):
        PvcConstruct(self,
                    name=self.pvc_name,
                    namespace=self.namespace,
                    storage_class_name="standard-rwo") 