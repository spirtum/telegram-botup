# Telegram-botup

Library for fast development and simple deployment of Telegram bots. She includes:

- **Dispatcher** for handlers registration and receiving incoming updates
- **Form** for working with Telegram API
- **Sender**-worker for asynchronus requests
- Other utils, types and etc

# Features

- Full support of types and methods telegram API
- Built-in **Sender**-worker for making requests like task by task
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
from botup import Dispatcher, Form
from botup.types import InputFile
from flask import Flask, request

from my_func import get_random_image
from config import TOKEN
from config import redis_connection as rdb

app = Flask(__name__)
dispatcher = Dispatcher()
form = Form(token=TOKEN, connection=rdb)


def start_handler(chat_id, update):
    form.push(
        func=form.send_message,
        chat_id=chat_id,
        text='Hi!\nTo get image press to /image'
    )


def send_image(chat_id, update):
    path = get_random_image()
    cache = rdb.get(f'cache:{path}')
    if cache:
        input_file = InputFile(file_id=cache)
        form.push(
            func=form.send_photo,
            chat_id=chat_id,
            photo=input_file.as_dict()
        )
    else:
        input_file = InputFile(path=path)
        resp = form.push(
            func=form.send_photo,
            chat_id=chat_id,
            photo=input_file.as_dict()
        ).wait()
        rdb.set(f'cache:{path}', resp.photo[-1].file_id)


dispatcher.register_command_handler('/image', send_image)
dispatcher.register_command_handler('*', start_handler)


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
$ botup set_webhook --help
```

* *How to test bot without requests?*


Use **fake_mode=True** on **Form** initialization

```
form = Form(..., fake_mode=True, ...)
```

Or use **--fake-mode** on **Sender** starting

```
$ botup run_sender --token $TOKEN --fake-mode
```