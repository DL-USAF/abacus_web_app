import logging
from importlib.util import find_spec

from flask import Flask

from app.auth_services.AuthServiceBase import load_auth_service

logging.basicConfig(level=logging.DEBUG)

auth_service = load_auth_service()

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'TESTING': True,
    'DEBUG': True
})

app.config.update(auth_service.get_oidc_config())
app.config['OIDC_CLIENT_SECRETS'] = auth_service.get_client_secrets()

oidc = auth_service.init_oidc(app)


@app.context_processor
def inject_oidc():
    mock_datawave = find_spec('datawave_cli') is None
    
    return {'oidc':oidc, 'mocking_datawave_cli':mock_datawave}

def create_app():
    from app.routes import main

    app.register_blueprint(main)
    return app