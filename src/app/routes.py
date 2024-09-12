from flask import render_template, Blueprint, redirect, url_for, request
from app import oidc

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


@main.route('/query', methods=['GET', 'POST'])
@oidc.require_login
def query():
    auths = ['FOO', 'BAR', 'PUBLIC', 'PRIVATE']

    if request.method == 'POST':
        query_name = request.form.get('query_name')
        query_text = request.form.get('query')
        selected_auths = [auth for auth in request.form.getlist('auths') if auth]
        data_type = request.form.get('data_type')
        output_location = request.form.get('output_location')
        decode_raw_data = 'decode_raw_data' in request.form

        return render_template('query_result.html', query_name=query_name,
                               query_text=query_text,
                               selected_auths=selected_auths,
                               data_type=data_type,
                               output_location=output_location,
                               decode_raw_data=decode_raw_data)
    else:
        return render_template('query.html', auths=auths)


@main.route('/upload')
@oidc.require_login
def upload():
    return render_template('upload.html')


@main.route('/logout')
def logout():
    oidc.logout()
    return redirect(url_for('main.index'))
