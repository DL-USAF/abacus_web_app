from .AuthServiceBase import AuthService

class KeycloakAuthService(AuthService):
    def get_oidc_config(self):
        return {
            'OIDC_ID_TOKEN_COOKIE_SECURE': False,
            'OIDC_USER_INFO_ENABLED': True,
            'OIDC_OPENID_REALM': 'external',
            'OIDC_SCOPES': ['openid', 'email', 'profile'],
            'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post'
        }

    def get_client_secrets(self):
        return {
            "web": {
                "issuer": "http://localhost:8080/realms/external",
                "auth_uri": "http://localhost:8080/realms/external/protocol/openid-connect/auth",
                "client_id": "flask-app",
                "client_secret": "zlZq3WjKZUtRbQPTRMoB7FW91xSsC0tp",
                "redirect_uris": [
                    "http://localhost:5000/*"
                ],
                "userinfo_uri": "http://localhost:8080/realms/external/protocol/openid-connect/userinfo", 
                "token_uri": "http://localhost:8080/realms/external/protocol/openid-connect/token",
                "token_introspection_uri": "http://localhost:8080/realms/external/protocol/openid-connect/token/introspect"
            }
        }