import click

from .sender import Sender
from .utils import setup_logging


@click.group()
def cli():
    """A telegram-botup command line tool"""
    pass


@cli.command('run_sender')
@click.option('--token', '-t', required=True, help='Your bot token')
@click.option('--redis-host', required=True, help='Redis host', default='localhost', show_default=True)
@click.option('--redis-port', required=True, help='Redis port', default='6379', show_default=True)
@click.option('--redis-db', required=True, help='Redis db', default='0', show_default=True)
@click.option('--socks-proxy-string', '-s', help='Connection string for use socks5 proxy server')
@click.option('--queue', '-q', required=True, help='Specific queue name', default='botup-sender-queue',
              show_default=True)
@click.option('--rate-limit', '-rt', required=True, default=0.5, type=float,
              help='Rate limit. One request per rate-limit', show_default=True)
@click.option('--quiet', help='Quiet mode', is_flag=True, default=False)
@click.option('--fake-mode', help='Fake start without requests', is_flag=True, default=False, show_default=True)
@click.option('--proxy-url', help='Proxy URL for requests')
@click.option('--basic-auth-string', help='Connection string for basic auth')
def run_sender(token, redis_host, redis_port, redis_db, socks_proxy_string, queue, rate_limit,
               quiet, fake_mode, proxy_url, basic_auth_string):
    """Start the sender"""
    if fake_mode:
        print('Run with --fake-mode')
    if not quiet:
        setup_logging()
    Sender.start_new_worker(
        token=token,
        redis_host=redis_host,
        redis_port=redis_port,
        redis_db=redis_db,
        queue=queue,
        rate_limit=rate_limit,
        proxy_url=proxy_url,
        basic_auth_string=basic_auth_string,
        socks_proxy_string=socks_proxy_string,
        fake_mode=fake_mode
    )


@cli.command('set_webhook')
@click.option('--token', '-t', required=True, help='Your bot token')
@click.option('--url', '-u', required=True, help='Your external url')
@click.option('--socks-proxy-string', '-s', help='Connection string for use socks5 proxy server')
@click.option('--proxy-url', help='Proxy URL for requests')
@click.option('--basic-auth-string', help='Connection string for basic auth')
def set_webhook(token, url, socks_proxy_string, proxy_url, basic_auth_string):
    """Set webhook"""
    if not url.endswith('/'):
        url = f'{url}/'
    url += token
    sender = Sender(
        token=token,
        proxy_url=proxy_url,
        basic_auth_string=basic_auth_string,
        socks_proxy_string=socks_proxy_string
    )
    resp = sender.set_webhook(url)
    if resp.is_error():
        print(resp.description)
    else:
        resp.pprint()


@cli.command('delete_webhook')
@click.option('--token', '-t', required=True, help='Your bot token')
@click.option('--socks-proxy-string', '-s', help='Connection string for use socks5 proxy server')
@click.option('--proxy-url', help='Proxy URL for requests')
@click.option('--basic-auth-string', help='Connection string for basic auth')
def delete_webhook(token, socks_proxy_string, proxy_url, basic_auth_string):
    """Delete webhook"""
    sender = Sender(
        token=token,
        proxy_url=proxy_url,
        basic_auth_string=basic_auth_string,
        socks_proxy_string=socks_proxy_string
    )
    resp = sender.delete_webhook()
    if resp.is_error():
        print(resp.description)
    else:
        resp.pprint()


@cli.command('send_message')
@click.option('--token', '-t', required=True, help='Your bot token')
@click.option('--chat-id', '-c', required=True, type=int, help='Chat id')
@click.option('--message', '-m', required=True, help='Message')
@click.option('--socks-proxy-string', '-s', help='Connection string for use socks5 proxy server')
@click.option('--proxy-url', help='Proxy URL for requests')
@click.option('--basic-auth-string', help='Connection string for basic auth')
def send_message(token, chat_id, message, socks_proxy_string, proxy_url, basic_auth_string):
    """Send message"""
    sender = Sender(
        token=token,
        proxy_url=proxy_url,
        basic_auth_string=basic_auth_string,
        socks_proxy_string=socks_proxy_string
    )
    resp = sender.send_message(chat_id, message)
    if resp.is_error():
        print(resp.description)
    else:
        resp.pprint()
