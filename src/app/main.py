from flask import render_template, Blueprint, redirect, url_for

from app import oidc,routes


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
    return routes.query.route()


@main.route('/query_results', methods=['GET', 'POST'])
@oidc.require_login
def query_results():
    return routes.query.route_results()


@main.route('/dictionary', methods=['GET', 'POST'])
@oidc.require_login
def dictionary():
    return routes.dictionary.route()


@main.route('/upload')
@oidc.require_login
def upload():
    return render_template('upload.html')


@main.route('/logout')
def logout():
    oidc.logout()
    return redirect(url_for('main.index'))
