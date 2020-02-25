import os
import subprocess
import pathlib

import click

from .sender import Sender
from .utils import setup_logging


@click.group()
def cli():
    """A telegram-botup command line tool"""
    pass


@cli.command('start')
@click.option('--file', '-f', help='Specify file location. ./botup.yml by default', default=None)
@click.option('--host', '-h', help='Specify host', required=True, default='0.0.0.0', show_default=True)
@click.option('--port', '-p', help='Specify port', required=True, default=5000, show_default=True)
@click.option('--processes', help='UWSGI processes count', required=True, default=1, show_default=True)
@click.option('--threads', help='UWSGI threads count', required=True, default=4, show_default=True)
@click.option('--uwsgi', help='Run with uwsgi', is_flag=True)
def cmd_start(file, host, port, processes, threads, uwsgi):
    """Start bot from yaml config file"""
    if not file:
        path = pathlib.Path('.') / 'botup.yml'
    else:
        path = pathlib.Path(file)
    if not path.exists():
        print(f'{path} does not exists')
        return
    from .wsgi import WSGIApp
    if uwsgi:
        subprocess.run(
            args=['uwsgi',
                  '--http', f'{host}:{port}',
                  '-w', 'botup.wsgi',
                  '--callable', 'app',
                  '--processes', str(processes),
                  '--threads', str(threads)],
            env={'BOTUP_YAML_FILE': str(path), 'PATH': os.environ.get('PATH', '')},
            stdout=subprocess.PIPE
        )
        return
    app = WSGIApp.from_yaml_file(str(path))
    app.run(host=host, port=port)


@cli.command('run_sender')
@click.option('--token', '-t', required=True, help='Your bot token')
@click.option('--redis-host', required=True, help='Redis host', default='localhost', show_default=True)
@click.option('--redis-port', required=True, help='Redis port', default='6379', show_default=True)
@click.option('--redis-db', required=True, help='Redis db', default='0', show_default=True)
@click.option('--redis-password', help='Redis password')
@click.option('--proxy-string', '-p', help='Connection string for use proxy server')
@click.option('--queue', '-q', help='Specific queue name', default=None)
@click.option('--rate-limit', '-rt', default=None, type=float, help='Rate limit. One request per rate-limit')
@click.option('--quiet', help='Quiet mode', is_flag=True, default=False)
@click.option('--fake-mode', help='Fake start without requests', is_flag=True, default=False)
def cmd_run_sender(token, redis_host, redis_port, redis_db, redis_password, proxy_string, queue, rate_limit,
               quiet, fake_mode):
    """Start the sender"""
    queue = queue or Sender.DEFAULT_QUEUE
    rate_limit = rate_limit or Sender.DEFAULT_RATE_LIMIT
    redis_cfg = {
        'host': redis_host,
        'port': redis_port,
        'db': redis_db,
        'password': redis_password,
        'decode_responses': True,
        'encoding': 'utf-8'
    }
    if fake_mode:
        print('Run with --fake-mode')
    if not quiet:
        setup_logging()
    Sender.start_new_worker(
        token=token,
        redis_cfg=redis_cfg,
        queue=queue,
        rate_limit=rate_limit,
        proxy_string=proxy_string,
        fake_mode=fake_mode
    )


@cli.command('set_webhook')
@click.option('--token', '-t', required=True, help='Your bot token')
@click.option('--url', '-u', required=True, help='Your external url')
@click.option('--proxy-string', '-p', help='Connection string for use proxy server')
def cmd_set_webhook(token, url, proxy_string):
    """Set webhook"""
    if not url.endswith('/'):
        url = f'{url}/'
    url += token
    sender = Sender(
        token=token,
        proxy_string=proxy_string
    )
    resp = sender.set_webhook(url)
    if resp.is_error():
        print(resp.description)
    else:
        resp.pprint()


@cli.command('delete_webhook')
@click.option('--token', '-t', required=True, help='Your bot token')
@click.option('--proxy-string', '-p', help='Connection string for use proxy server')
def cmd_delete_webhook(token, proxy_string):
    """Delete webhook"""
    sender = Sender(
        token=token,
        proxy_string=proxy_string
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
@click.option('--proxy-string', '-p', help='Connection string for use proxy server')
def cmd_send_message(token, chat_id, message, proxy_string):
    """Send message"""
    sender = Sender(
        token=token,
        proxy_string=proxy_string
    )
    resp = sender.send_message(chat_id, message)
    if resp.is_error():
        print(resp.description)
    else:
        resp.pprint()
