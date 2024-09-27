import click
import json
from pathlib import Path
from types import SimpleNamespace


@click.group
@click.option('-s', '--suppress-warning', is_flag=True, hidden=True,
              help="If passed will suppress the certificate verification warning. Does not show on --help.")
def main(**kwargs):
    pass


def common_options(f):
    """A decorator for adding options common to most submodules"""
    f = click.option("-u", "--url", type=str)(f)
    f = click.option("-i", "--ip", is_flag=True)(f)
    f = click.option('-n', '--namespace', type=str)(f)
    f = click.option("--log-level", default="INFO")(f)
    f = click.option("-k", "--key", type=str)(f)
    f = click.option("-c", "--cert", type=str, required=True)(f)
    return f


@main.command
@common_options
@click.option("-q", "--query", type=str, required=True)
@click.option("--query-name", type=str, default="test-query")
@click.option("--auths", type=str, required=True)
@click.option("-f", "--filter", type=str, default=None)
@click.option("-o", "--output", type=str)
@click.option("--html", is_flag=True)
@click.option("-d", "--decode-raw", is_flag=True)
def query(**kwargs):
    parent_path = Path(__file__).parent
    with open(parent_path.joinpath('sample_query.json'), 'r') as f:
        res = json.load(f)
    return res


@main.command
@common_options
def authorization(**kwargs):
    parent_path = Path(__file__).parent
    with open(parent_path.joinpath("sample_authorization.json"), 'r') as f:
        res = json.load(f)
    return res


@main.command
@common_options
@click.option("--auths", type=str, required=True)
@click.option("-d", "--data-types", type=str)
def dictionary(**kwargs):
    parent_path = Path(__file__).parent
    with open(parent_path.joinpath('sample_dict.json'), 'r') as f:
        res = json.load(f)
    return res