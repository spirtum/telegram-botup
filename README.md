# Telegram-botup

Library for fast development and simple deployment of Telegram bots. She includes:

- **Dispatcher** handles incoming updates
- **Sender** works with Telegram API
- Other utils, types and etc

# Features

- Full support of types and methods telegram API
- Built-in worker for making requests like task by task
- State control dispatching
- Regexp dispatching
- Simple switching between synchronus and asynchronus work
- Simple deployment with wsgi
- Built-in command-line tool
- Support of work with socks5-proxy and proxy-url



# Installation
```
$ pip install telegram-botup
```

# Example
```
import re

from botup import Dispatcher, Sender
from botup.types import InputFile
from flask import Flask, request

from my_func import get_random_image
from config import TOKEN
from config import redis_connection as rdb

app = Flask(__name__)
dispatcher = Dispatcher()
sender = Sender(token=TOKEN, connection=rdb)


def start_handler(chat_id, update):
    sender.push(
        func=sender.send_message,
        chat_id=chat_id,
        text='Hi!\nTo get image press to /image'
    )


def send_image(chat_id, update):
    path = get_random_image()
    cache = rdb.get(f'cache:{path}')
    if cache:
        input_file = InputFile(file_id=cache)
        sender.push(
            func=sender.send_photo,
            chat_id=chat_id,
            photo=input_file.as_dict()
        )
    else:
        input_file = InputFile(path=path)
        resp = sender.push(
            func=sender.send_photo,
            chat_id=chat_id,
            photo=input_file.as_dict()
        ).wait()
        rdb.set(f'cache:{path}', resp.photo[-1].file_id)


dispatcher.register_command_handler('/image', send_image)
dispatcher.register_command_handler(re.compile('.*'), start_handler)


@app.route(f'/{TOKEN}', methods=['POST'])
def index():
    try:
        req = request.get_json()
        dispatcher.handle(req)
    except Exception as exc:
        import traceback
        print(traceback.format_exc())
    return "!", 200

```

## Q/A

* *How to set webhook?*

```
$ botup --help
```
