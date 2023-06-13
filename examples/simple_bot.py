from web_lib import App, Request
from botup.core.dispatcher import Dispatcher
from botup.core.api import Api
from botup.core.types import CoreContext

TOKEN = "token"

app = App()
dispatcher = Dispatcher()
api = Api(TOKEN)


@dispatcher.message_handler('hello')
async def hello_handler(ctx: CoreContext):
    await api.send_message(ctx.chat_id, f'Hello {ctx.update.message.from_.first_name}')


@app.post(f'/{TOKEN}')
async def index(request: Request):
    await dispatcher.handle(await request.json())
    return "!"
