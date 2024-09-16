from .AuthServiceBase import AuthService, CustomOpenIDConnect
from flask import session
from datetime import datetime, timedelta


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
    def __init__(self, *args, **kwargs):
        super(MockOpenIDConnect, self).__init__(*args, **kwargs)
        self.mock_user = {
            "sub": "12345",
            "email": "mockuser@example.com",
            "name": "Mock User",
        }
        self.mock_token = {
            "exp": datetime.now() + timedelta(days=365),
            "id_token": "mock_id_token",
        }

    @property
    def user_loggedin(self):
        session['oidc_auth_profile'] = self.user_getinfo(None)
        return True

    def check_token_expiry(self):
        session['oidc_auth_token'] = self.mock_token
        return super(MockOpenIDConnect, self).check_token_expiry()

    def ensure_active_token(self, token=None):
        return True

    def token_is_valid(self, token=None):
        return True

    def user_getinfo(self, fields):
        return self.mock_user
