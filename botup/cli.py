import sys
import asyncio
import pprint
from typing import List

from .exceptions import ParseArgsException
from .sender import Sender


HELP_MESSAGE = """
Botup cli utility

$ botup <command> ...args

Commands:
    set_webhook
    delete_webhook
    send_message
    help
    
Examples:
    $ botup set_webhook -t <token> -u <url>
    $ botup delete_webhook -t <token>
    $ botup send_message -t <token> -c <chat_id> -m <message>
""".strip()

WRONG_COMMAND_MESSAGE = """
Command not found.

Usage:
    $ botup help
""".strip()

WRONG_ARGS_MESSAGE = """
Error while parsing args. 

Usage:
    $ botup help
""".strip()


async def cmd_set_webhook(token: str, url: str):
    """Set webhook"""

    url = url + '/' if not url.endswith('/') else url
    url += token

    sender = Sender(token)

    resp = await sender.set_webhook(url)
    pprint.pprint(resp.as_dict())


async def cmd_delete_webhook(token: str):
    """Delete webhook"""

    sender = Sender(token)

    resp = await sender.delete_webhook()
    pprint.pprint(resp.as_dict())


async def cmd_send_message(token: str, chat_id: str, message: str):
    """Send message"""

    sender = Sender(token)
    resp = await sender.send_message(chat_id, message)
    pprint.pprint(resp.as_dict())


async def cmd_help():
    """Help page"""
    print(HELP_MESSAGE)


CMD_MAP = {
    'set_webhook': {
        'func': cmd_set_webhook,
        'args': {
            '-t': 'token',
            '-u': 'url'
        },
        'required': ['token', 'url']
    },
    'delete_webhook': {
        'func': cmd_delete_webhook,
        'args': {
            '-t': 'token'
        },
        'required': ['token']
    },
    'send_message': {
        'func': cmd_send_message,
        'args': {
            '-t': 'token',
            '-c': 'chat_id',
            '-m': 'message'
        },
        'required': ['token', 'chat_id', 'message']
    },
    'help': {
        'func': cmd_help,
        'args': {},
        'required': []
    }
}


def parse_args(args: str, expected_args: dict, required: List[str]) -> dict:
    args_length = len(args)

    if expected_args and not args_length:
        raise ParseArgsException()

    if not args_length:
        return {}

    if args_length % 2 != 0:
        raise ParseArgsException()

    result = {}
    index = 0
    while True:
        if index + 2 > args_length:
            break

        flag, value = args[index], args[index+1]
        if flag not in expected_args:
            raise ParseArgsException()

        result[expected_args[flag]] = value
        index += 2

    for arg in required:
        if arg not in result:
            raise ParseArgsException()

    return result


def main():
    if len(sys.argv) == 1:
        print(HELP_MESSAGE)
        return

    _, command, *args = sys.argv
    info = CMD_MAP.get(command)
    if not info:
        print(WRONG_COMMAND_MESSAGE)
        return

    func = info['func']
    expected_args = info['args']
    required = info['required']

    try:
        parsed_args = parse_args(args, expected_args, required)
    except ParseArgsException:
        print(WRONG_ARGS_MESSAGE)
        return

    asyncio.run(func(**parsed_args))
