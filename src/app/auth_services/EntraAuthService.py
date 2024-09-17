import json
import os
from .AuthServiceBase import AuthService
from . import logger


class EntraAuthService(AuthService):

    def get_oidc_config(self):
        return {
            'OIDC_ID_TOKEN_COOKIE_SECURE': False,
            'OIDC_USER_INFO_ENABLED': True,
            'OIDC_OPENID_REALM': 'external',
            'OIDC_SCOPES': ['openid', 'email', 'profile'],
            'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post'
        }

    def get_client_secrets(self):
        logger.info("Setting up the client_secrets for Keycloak.")
        config_file = os.path.join(os.getcwd(), "configs/entra_config.json")
        logger.info(config_file)
        if os.path.exists(config_file):
            return self.read_config_file(config_file)
        else:
            base_url = "http://localhost:8080/realms"
            return {
                "web": {
                    "issuer": f"{base_url}/external",
                    "auth_uri": f"{base_url}/external/protocol/openid-connect/auth",
                    "client_id": "flask-app",
                    "client_secret": "zlZq3WjKZUtRbQPTRMoB7FW91xSsC0tp",
                    "redirect_uris": [
                        "http://localhost:5000/*"
                    ],
                    "userinfo_uri": f"{base_url}/external/protocol/openid-connect/userinfo",
                    "token_uri": f"{base_url}/external/protocol/openid-connect/token",
                    "token_introspection_uri": f"{base_url}/external/protocol/openid-connect/token/introspect"
                }
            }