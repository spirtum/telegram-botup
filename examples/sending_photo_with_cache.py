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
