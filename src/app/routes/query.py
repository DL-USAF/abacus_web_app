import os
import re
from uuid import uuid4
from flask import render_template, request, flash, redirect, url_for
from click.testing import CliRunner
from cryptography.fernet import Fernet
from hdfs import InsecureClient
from werkzeug.utils import secure_filename



from app import routes_logger

try:
    from datawave_cli.main import main as dwv_entry_point
except Exception:
    from mock.datawave_cli.main import main as dwv_entry_point


def route():
    cmd = 'authorization -c [PLACEHOLDER] -k [PLACEHOLDER]'.split(' ')
    whoami = CliRunner().invoke(dwv_entry_point, cmd, standalone_mode=False).return_value
    auths = whoami['proxiedUsers'][0]['auths']

    return render_template('query.html', auths=auths)


def route_results():
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
