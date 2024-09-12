import os
import importlib
from abc import ABC, abstractmethod
from flask_oidc import OpenIDConnect


class AuthService(ABC):
    @abstractmethod
    def get_oidc_config(self):
        """Returns the OIDC configuration to be used in app.config.update."""
        pass

    @abstractmethod
    def get_client_secrets(self):
        """Returns the client secrets as a dictionary."""
        pass

    def init_oidc(self, app):
        """Initializes the OIDC object"""
        return CustomOpenIDConnect(app, client_secrets=self.get_client_secrets())


class CustomOpenIDConnect(OpenIDConnect):
    """A custom implementation of the OpenIDConnect class that accepts a client_secrets dictionary"""
    def __init__(self, app=None, client_secrets=None, *args, **kwargs):
        self.client_secrets_data = client_secrets
        super().__init__(app, *args, **kwargs)

    def load_secrets(self, app):
        return self.client_secrets_data


def load_auth_service():
    # auth_service = os.getenv('AUTH_SERVICE', 'MockAuthService')
    auth_service = 'DexAuthService'

    try:
        module = importlib.import_module(f'app.auth_services.{auth_service}')
        auth_service_class = getattr(module, auth_service)
        return auth_service_class()
    except (ImportError, AttributeError) as e:
        print(e)
        raise ValueError(f"Unknown authentication service class: {auth_service}")