#!/usr/bin/env python3
from constructs import Construct

from imports.io.istio import security as sc


class AuthorizationPolicyConstruct(Construct):

    def __init__(self, scope: Construct, *,
                namespace: str,
                app_name: str):
        id = "AuthorizationPolicy"
        super().__init__(scope, id)

        sc.AuthorizationPolicy(
            self, id,
            metadata={"name": "pytorch-policy", "namespace": namespace},
            spec=sc.AuthorizationPolicySpec(
              action=sc.AuthorizationPolicySpecAction("ALLOW"),
              selector=sc.AuthorizationPolicySpecSelector(match_labels={"app": app_name}),
              rules=[
                sc.AuthorizationPolicySpecRules(
                  to=[sc.AuthorizationPolicySpecRulesTo(operation=sc.AuthorizationPolicySpecRulesToOperation(methods=["GET","POST"], paths=["/pytorch/*"]))],
                  when=[sc.AuthorizationPolicySpecRulesWhen(key="request.auth.claims[permissions]", values=["inference:pytorch"])]
                )
              ]
            )
        )