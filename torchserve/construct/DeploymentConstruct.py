#!/usr/bin/env python3
from constructs import Construct

from imports import k8s

class DeploymentConstruct(Construct):

    def __init__(self, scope: Construct, *,
                name: str, 
                metadata: k8s.ObjectMeta, 
                label: dict, 
                image: str, 
                pvc_name: str,
                volume_mount_name: str,
                replicas=1, 
                cpu=1, 
                memory="4Gi"):
        super().__init__(scope, "deployment")
        
        containers = [
            k8s.Container(
                name=name,
                image=image,
                ports=[
                    k8s.ContainerPort(name="ts",container_port=8080),
                    k8s.ContainerPort(name="ts-management",container_port=8081),
                    k8s.ContainerPort(name="ts-metrics",container_port=8082),
                ],
                args=["torchserve --start --model-store /home/model-server/shared/model-store/"],
                image_pull_policy="IfNotPresent",
                volume_mounts=[
                    k8s.VolumeMount(mount_path="/home/model-server/shared/", name=volume_mount_name)
                ],
                resources=k8s.ResourceRequirements(limits={
                    "cpu": k8s.Quantity.from_number(cpu),
                    "memory": k8s.Quantity.from_string(memory)
                })
            )
        ]
        pod_spec = k8s.PodSpec(
            security_context=k8s.PodSecurityContext(
                run_as_user=1000,
                run_as_group=3000,
                fs_group=2000,
                fs_group_change_policy="OnRootMismatch"
            ),
            containers=containers,
            volumes=[
                k8s.Volume(
                    name=volume_mount_name,
                    persistent_volume_claim=k8s.PersistentVolumeClaimVolumeSource(claim_name=pvc_name)
                )
            ]
        )

        k8s.KubeDeployment(
            self, "deployment",
            metadata=metadata,
            spec=k8s.DeploymentSpec(
                replicas=replicas,
                selector=k8s.LabelSelector(match_labels=label),
                template=k8s.PodTemplateSpec(
                    metadata=k8s.ObjectMeta(labels=label),
                    spec=pod_spec
                )
            )
        )