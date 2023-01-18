#!/usr/bin/env python3
from constructs import Construct

from imports.io.istio import security

class RequestAuthenticationConstruct(Construct):

    def __init__(self, scope: Construct, *,
                namespace: str,
                app_name: str):
        super().__init__(scope, "RequestAuthentication")

        label={"app": app_name}
        security.RequestAuthentication(
            self, "RequestAuthentication",
            metadata={"name": "auth0", "namespace": namespace},
            spec=security.RequestAuthenticationSpec(selector=security.RequestAuthenticationSpecSelector(match_labels=label),
            jwt_rules=[
              security.RequestAuthenticationSpecJwtRules(issuer="https://{auth0-domain-url}",
                                                        jwks_uri="https://{auth0-domain-url}/.well-known/jwks.json")
            ])
        )