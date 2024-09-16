import importlib
import json
import os
from pathlib import Path
from abc import ABC, abstractmethod
from flask_oidc import OpenIDConnect
from . import logger


class AuthService(ABC):
    def __init__(self):
        pass

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

    def read_config_file(self, auth_config_file: str):
        """Reads in the configuration file."""
        logger.debug("Auth Config file found!")
        with open(auth_config_file, 'r') as f:
            return json.load(f)


class CustomOpenIDConnect(OpenIDConnect):
    """A custom implementation of the OpenIDConnect class that accepts a client_secrets dictionary"""
    def __init__(self, app=None, client_secrets=None, *args, **kwargs):
        self.client_secrets_data = client_secrets
        super().__init__(app, *args, **kwargs)

    def load_secrets(self, app):
        return self.client_secrets_data


def load_auth_service():
    auth_service = os.getenv('AUTH_SERVICE', 'MockAuthService')

    try:
        module = importlib.import_module(f'app.auth_services.{auth_service}')
        auth_service_class = getattr(module, auth_service)
        return auth_service_class()
    except (ImportError, AttributeError) as e:
        print(e)
        raise ValueError(f"Unknown authentication service class: {auth_service}")