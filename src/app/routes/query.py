import base64
import io
import zipfile
from uuid import uuid4
from flask import render_template, request, flash, redirect, url_for, jsonify, send_file
from click.testing import CliRunner


from app import routes_logger

try:
    from datawave_cli.main import main as dwv_entry_point
except Exception:
    from mock.datawave_cli.main import main as dwv_entry_point


def route():
    # TODO: Correctly reference certs
    cmd = 'authorization -c [PLACEHOLDER] -k [PLACEHOLDER]'.split(' ')
    whoami = CliRunner().invoke(dwv_entry_point, cmd, standalone_mode=False).return_value
    auths = whoami['proxiedUsers'][0]['auths']

    return render_template('query.html', auths=auths)


def route_results():
    # We need to handle our args in a few different ways, first and foremost if they are passed as args in the url
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

    # TODO: Add the rest of the CLI options for query

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

        # TODO: Correctly reference certs
        cmd = [
            'query',
            '-c', 'PLACEHOLDER', '-k', 'PLACEHOLDER',
            '-q', query,
            '--query-name', f'{query_name}',
            '--auths', ",".join(selected_auths),
            f'-f {data_type}' if data_type else ''
        ]
        cmd = list(filter(lambda item: item, cmd))
        output = CliRunner().invoke(dwv_entry_point, cmd, standalone_mode=False).return_value

        if user_requests_json(request):
            return jsonify(output)

        starting_cols = ['NAME', 'VISIBILITY']
        ending_cols = ['TERM_COUNT', 'LOAD_DATE', 'ORIG_FILE', 'RECORD_ID']

        events = output['events']
        all_cols = set(events[0].keys()).union(*(d.keys() for d in events[1:]))

        COLUMN_ORDER = [col for col in starting_cols if col in all_cols]
        if any(col.startswith('RAWDATA_') for col in all_cols):
            COLUMN_ORDER.append('RAWDATA')
        for col in all_cols:
            # We should only add the column if it is not defined in start_cols, end_cols, and does not contain raw data
            should_add = col not in starting_cols
            should_add &= col not in ending_cols
            should_add &= not col.startswith('RAWDATA_')
            if should_add:
                COLUMN_ORDER.append(col)
        COLUMN_ORDER.extend([col for col in ending_cols if col in all_cols])

        return render_template('query_result.html', data=output, column_order=COLUMN_ORDER)


def user_requests_json(request):
    valid = request.path.endswith('.json')
    valid |= request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']
    return valid


def download_raw():
    events = request.json.get('events', [])
    zip_name = request.json.get('zip_name', 'raw_data.zip')

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for event in events:
            """
            We need a way to uniquely name each of our events. Conveniently dwv's ORIG_FILE provides that!
            The field is of the form [file_name]|[event_number]|[upload_number].
            upload_number is in case a file with the same name but different content was uploaded multiple
            times. Most of the time it's going to be 0 so we are not going to include it.
            """
            file_name, event_number, *_ = event['ORIG_FILE'].split('|')
            file_name = file_name.replace('.json', '')
            name = f'{file_name}_{event_number}'
            for column, data in event.items():
                if column.startswith('RAWDATA_'):
                    file_data = base64.b64decode(data)

                    parent_dir = f'{name}/' if f'{zip_name}' == 'raw_data.zip' else ''
                    zip_file.writestr(f'{parent_dir}{column}.parquet', file_data)

    # Apparently we need to reset the buffer to 0...
    zip_buffer.seek(0)
    return send_file(zip_buffer, as_attachment=True, download_name=zip_name, mimetype='application/zip')
