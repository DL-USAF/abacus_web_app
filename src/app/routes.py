from uuid import uuid4

from flask import render_template, Blueprint, redirect, url_for, request, flash
from click.testing import CliRunner
import pandas as pd

from app import oidc, routes_logger

try:
    from datawave_cli.main import main as dwv_entry_point
except Exception:
    from mock.datawave_cli.main import main as dwv_entry_point

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/login')
@oidc.require_login
def login():
    return redirect(url_for('main.dashboard'))


@main.route('/dashboard')
@oidc.require_login
def dashboard():
    return render_template('dashboard.html')


@main.route('/query')
@oidc.require_login
def query():
    cmd = 'authorization -c [PLACEHOLDER] -k [PLACEHOLDER]'.split(' ')
    whoami = CliRunner().invoke(dwv_entry_point, cmd, standalone_mode=False).return_value
    auths = whoami['proxiedUsers'][0]['auths']

    return render_template('query.html', auths=auths)


@main.route('/query_results', methods=['GET', 'POST'])
@oidc.require_login
def query_results():
    if request.method == 'POST':
        query_name = request.form.get('query_name') or uuid4()
        query_text = request.form.get('query')
        selected_auths = [auth for auth in request.form.getlist('auths') if auth]

        if not selected_auths:
            flash('Please select at least one Auth option.', 'error')
            return redirect(url_for('main.query'))

        data_type = request.form.get('data_type')
        decode_raw_data = bool(request.form.get('decode_raw_data'))

        output_location = f'/tmp/{query_name}/results.json'
        cmd = [
            'query',
            '-c', 'PLACEHOLDER', '-k', 'PLACEHOLDER',
            '-q', query_text,
            '--query-name', f'{query_name}',
            '--auths', ",".join(selected_auths),
            f'-f {data_type}' if data_type else '',
            f'{"-d" if decode_raw_data else ""}',
            '-o', output_location, '--html'
        ]
        cmd = list(filter(lambda item: item, cmd))
        output_html = CliRunner().invoke(dwv_entry_point, cmd, standalone_mode=False).return_value

        return render_template('query_result.html', output_location=output_location, output_html=output_html)
    else:
        return render_template('query_result.html', no_query=True)


@main.route('/dictionary', methods=['GET', 'POST'])
@oidc.require_login
def dictionary():
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


@main.route('/upload')
@oidc.require_login
def upload():
    return render_template('upload.html')


@main.route('/logout')
def logout():
    oidc.logout()
    return redirect(url_for('main.index'))
