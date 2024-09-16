import click


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
def query(url, ip, namespace, log_level, key, cert, query, query_name, auths, filter, output, html, decode_raw):
    print('in query')
    return f"""
    <ul style="list-style-type: none;">
        <li><strong>Query Name:</strong> {query_name}</li>
        <li><strong>Query Text:</strong> {query}</li>
        <li><strong>Selected Auths:</strong> {auths}</li>
        <li><strong>Data Type:</strong> {"All" if not filter else filter}</li>
        <li><strong>Output Location:</strong> {output}</li>
        <li><strong>Decode Raw Data:</strong> {decode_raw}</li>
    </ul>
    """


@main.command
@common_options
def authorization(**kwargs):
    res = {'proxied_users': [{'auths': ['FOO', 'BAR', 'PUBLIC', 'PRIVATE']}]}
    return (res)