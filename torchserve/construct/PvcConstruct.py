#!/usr/bin/env python3
from constructs import Construct

from imports import k8s

class PvcConstruct(Construct):

    def __init__(self, scope: Construct, *, 
                name: str,
                namespace: str, 
                storage_class_name: str, 
                access_modes=["ReadWriteOnce"],
                storage="10Gi"):
        super().__init__(scope, "pvc")

        metadata = k8s.ObjectMeta(name=name, namespace=namespace)

        k8s.KubePersistentVolumeClaim(self, "PersistentVolumeClaim",
          metadata=metadata,
          spec=k8s.PersistentVolumeClaimSpec(
            access_modes=access_modes,
            storage_class_name=storage_class_name,
            resources=k8s.ResourceRequirements(requests={"storage":k8s.Quantity.from_string(storage)})
          )
        )