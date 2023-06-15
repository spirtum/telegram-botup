from web_lib import App, Request

from botup.dispatcher import Dispatcher
from botup.api import Api
from botup.types import BaseContext

TOKEN = "token"

app = App()
api = Api(TOKEN)
dispatcher = Dispatcher()


@dispatcher.message_handler('hello')
async def hello_handler(ctx: BaseContext):
    await api.send_message(ctx.chat_id, f'Hello {ctx.update.message.from_.first_name}')


@app.post(f'/{TOKEN}')
async def index(request: Request):
    await dispatcher.handle(await request.json())
    return ""
