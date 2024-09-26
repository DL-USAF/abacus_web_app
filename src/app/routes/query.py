from uuid import uuid4
from flask import render_template, request, flash, redirect, url_for, jsonify
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

    return render_template('query.html', auths=auths)


def route_results():
    # We need to handle our args in a few different ways, first and formost if they are passed as args in the url
    arg_source = request.args.copy()

    # Next, if we're given a form we should use that
    if request.form:
        arg_source.update(request.form)

    # and finally if we're given json we should handle that
    if request.is_json:
        json_data = request.get_json()
        if json_data:
            arg_source.update(json_data)

    # If we don't have any args at this point we should say there was no query to run
    if not arg_source:
        return render_template('query_result.html', no_query=True)

    # Extract our arguments
    query_name = arg_source.get('query_name') or uuid4()
    query = arg_source.get('query')
    data_type = arg_source.get('data_type')
    decode_raw_data = bool(arg_source.get('decode_raw_data'))

    # Users must provide Auths to run a query
    selected_auths = [auth for auth in arg_source.getlist('auths') if auth]
    if not selected_auths:
        flash('Please select at least one Auth option.', 'error')
        return redirect(url_for('main.query'))

    if request.method == 'POST':
        # POST requests are redirected to a GET with URL arguments so the users can copy their query URL if they want
        # If they want a json response we need to pass that along by using the `.json` endpoint
        endpoint = 'main.query_results' + ('_json' if user_requests_json(request) else '')
        return redirect(url_for(endpoint, query=query, auths=selected_auths,
                                query_name=query_name, data_type=data_type, decode_raw_data=decode_raw_data))
    elif request.method == 'GET':
        # GET requests execute the query
        output_location = f'/tmp/{query_name}/results.json'
        cmd = [
            'query',
            '-c', 'PLACEHOLDER', '-k', 'PLACEHOLDER',
            '-q', query,
            '--query-name', f'{query_name}',
            '--auths', ",".join(selected_auths),
            f'-f {data_type}' if data_type else '',
            f'{"-d" if decode_raw_data else ""}',
            '-o', output_location
        ]
        cmd = list(filter(lambda item: item, cmd))
        output = CliRunner().invoke(dwv_entry_point, cmd, standalone_mode=False).return_value

        if user_requests_json(request):
            return jsonify(output)

        COLUMN_ORDER = ['NAME', 'VISIBILITY']  # Starting columns
        COLUMN_ORDER += [None]  # Placeholder for unordered columns, 
        COLUMN_ORDER += ['TERM_COUNT', 'LOAD_DATE', 'ORIG_FILE', 'RECORD_ID']  # Ending columns

        return render_template('query_result.html',
                               metadata=output['metadata'], events=output['events'], column_order=COLUMN_ORDER)


def user_requests_json(request):
    valid = request.path.endswith('.json')
    valid |= request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']
    return valid