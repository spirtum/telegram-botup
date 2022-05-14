import re

from botup import Dispatcher, Sender
from botup.types import InputFile
from fastapi import FastAPI, Request

from my_func import get_random_image
from config import TOKEN
from config import redis_connection as rdb

app = FastAPI()
dispatcher = Dispatcher()
sender = Sender(token=TOKEN)


@dispatcher.command_handler('/image')
async def send_image(chat_id, update):
    path = get_random_image()
    cache = rdb.get(f'cache:{path}')
    if cache:
        input_file = InputFile(file_id=cache)
        await sender.send_photo(
            chat_id=chat_id,
            photo=input_file.as_dict()
        )
    else:
        input_file = InputFile(path=path)
        resp = await sender.send_photo(
            chat_id=chat_id,
            photo=input_file.as_dict()
        )
        rdb.set(f'cache:{path}', resp.photo[-1].file_id)


@dispatcher.command_handler(re.compile('.*'))
def start_handler(chat_id, update):
    sender.push(
        func=sender.send_message,
        chat_id=chat_id,
        text='Hi!\nTo get image press to /image'
    )


@app.post(f'/{TOKEN}')
async def index(request: Request):
    await dispatcher.handle(await request.json())
    return "!"
