from .AuthServiceBase import AuthService, CustomOpenIDConnect
from flask import session
from flask_oidc import OpenIDConnect


class MockAuthService(AuthService):
    def get_oidc_config(self):
        """Returns the OIDC configuration to be used in app.config.update"""
        return {}

    def get_client_secrets(self):
        """Returns the client secrets as a dictionary"""
        return {
            "web": {
                "issuer": "http://localhost:5000/mock",
                "auth_uri": "http://localhost:5000/mock/auth",
                "client_id": "mock-client-id",
                "client_secret": "mock-client-secret",
                "redirect_uris": [
                    "http://localhost:5000/*"
                ],
                "userinfo_uri": "http://localhost:5000/mock/userinfo",
                "token_uri": "http://localhost:5000/mock/token",
                "token_introspection_uri": "http://localhost:5000/mock/introspect"
            }
        }

    def init_oidc(self, app):
        """Returns a mocked version of the OpenIDConnect object"""
        return MockOpenIDConnect(app, self.get_client_secrets())


class MockOpenIDConnect(CustomOpenIDConnect):
    @property
    def user_loggedin(self):
        session['oidc_auth_profile'] = self.user_getinfo(None)
        return True

    def user_getinfo(self, fields):
        return {'preferred_username': 'mockuser',
                'email': 'mockuser@example.com',
                'sub': '1234567890'
                }