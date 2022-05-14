from fastapi import FastAPI, Request
from botup import Dispatcher, Sender

TOKEN = "token"

app = FastAPI()
dispatcher = Dispatcher()
sender = Sender(TOKEN)


@dispatcher.message_handler('hello')
async def hello_handler(chat_id, update):
    await sender.send_message(chat_id, f'Hello {update.message.from_.first_name}')


@app.post(f'/{TOKEN}')
async def index(request: Request):
    await dispatcher.handle(await request.json())
    return "!"
