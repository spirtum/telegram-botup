import re

import redis
from flask import Flask, request
from botup import Sender, Dispatcher, StateDispatcher, StateManager


TOKEN = ''
rdb = redis.StrictRedis()

KEY_MAIN = 'main'
KEY_FOO = 'foo'
KEY_BAR = 'bar'

app = Flask(__name__)
sender = Sender(TOKEN)
sm = StateManager(rdb)
dp_main = StateDispatcher(sm, KEY_MAIN)
dp_foo = Dispatcher()
dp_bar = Dispatcher()

dp_main.register_state(KEY_FOO, dp_foo)
dp_main.register_state(KEY_BAR, dp_bar)


def bar_handler(chat_id, update):
    sender.send_message(chat_id, 'is bar')


def foo_handler(chat_id, update):
    sender.send_message(chat_id, 'is foo')


def cmd_bar(chat_id, update):
    sm.set(KEY_MAIN, KEY_BAR)
    sender.send_message(chat_id, 'done')


def cmd_foo(chat_id, update):
    sm.set(KEY_MAIN, KEY_FOO)
    sender.send_message(chat_id, 'done')


def start(chat_id, update):
    text = '- /foo\n- /bar'
    sender.send_message(chat_id, text)


def back(chat_id, update):
    sm.reset(KEY_MAIN)
    start(chat_id, update)


dp_main.register_message_handler(re.compile('.*'), start)
dp_main.register_command_handler('/foo', cmd_foo)
dp_main.register_command_handler('/bar', cmd_bar)

dp_foo.register_message_handler(re.compile('.*'), foo_handler)
dp_foo.register_command_handler('/back', back)

dp_bar.register_message_handler(re.compile('.*'), bar_handler)
dp_bar.register_command_handler('/back', back)


@app.route(f'/{TOKEN}', methods=['POST'])
def index():
    try:
        req = request.get_json()
        dp_main.handle(req)
    except Exception as exc:
        import traceback
        print(traceback.format_exc())
    return "!", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
