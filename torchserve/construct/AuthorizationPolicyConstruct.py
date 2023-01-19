#!/usr/bin/env python3
from constructs import Construct

from imports.io.istio import security as sc


class AuthorizationPolicyConstruct(Construct):

    def __init__(self, scope: Construct, *,
                namespace: str,
                app_name: str,
                action: str,
                rules_key = "request.auth.claims[permissions]",
                rules_values: list):
        id = "AuthorizationPolicy"
        super().__init__(scope, id)

        sc.AuthorizationPolicy(
            self, id,
            metadata={"name": "pytorch-policy", "namespace": namespace},
            spec=sc.AuthorizationPolicySpec(
              action=sc.AuthorizationPolicySpecAction(action),
              selector=sc.AuthorizationPolicySpecSelector(match_labels={"app": app_name}),
              rules=[
                sc.AuthorizationPolicySpecRules(
                  when=[sc.AuthorizationPolicySpecRulesWhen(key=rules_key, values=rules_values)]
                )
              ]
            )
        )