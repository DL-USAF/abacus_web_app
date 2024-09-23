from flask import render_template, request
from click.testing import CliRunner

from app import routes_logger

try:
    from datawave_cli.main import main as dwv_entry_point
except Exception:
    from mock.datawave_cli.main import main as dwv_entry_point


def route():
    cmd = 'authorization -c [PLACEHOLDER] -k [PLACEHOLDER]'.split(' ')
    whoami = CliRunner().invoke(dwv_entry_point, cmd, standalone_mode=False).return_value
    auths = whoami['proxiedUsers'][0]['auths']

    data = ''
    if request.method == 'POST':
        selected_auths = [auth for auth in request.form.getlist('auths') if auth]
        datatypes = request.form.get('filter').replace(' ', '')
        cmd = 'dictionary'
        cmd += f' -c PLACEHOLDER -k PLACEHOLDER'
        cmd += f' --auths {",".join(selected_auths)}'
        cmd += f' -d {datatypes}' if datatypes else ''
        routes_logger.info(f'Executing {cmd}')
        data = CliRunner().invoke(dwv_entry_point, cmd, standalone_mode=False).return_value

    return render_template('dictionary.html', auths=auths, data=data)