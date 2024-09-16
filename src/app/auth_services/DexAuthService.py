from .AuthServiceBase import AuthService


class DexAuthService(AuthService):
    def get_oidc_config(self):
        return {
            'OIDC_OPENID_REALM': 'flask-app',
            'OIDC_SCOPES': ['openid', 'email', 'profile'],
            'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
        }

    def get_client_secrets(self):
        return {
            "web": {
                "issuer": "http://localhost:5556",
                "auth_uri": "http://localhost:5556/auth",
                "client_id": "flask-app",
                "client_secret": "flask-app-secret",
                "redirect_uris": [
                    "http://localhost:5000/*"
                ],
                "userinfo_uri": "http://localhost:5556/userinfo",
                "token_uri": "http://localhost:5556/token",
                "token_introspection_uri": "http://localhost:5556/token/introspect"
            }
        }
