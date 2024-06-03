# Telegram-botup

## Install
```
$ pip install telegram-botup
```

## Example
```python
# app.py

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
```


## Widgets example
```python
# app.py

from asyncio import gather

from web_lib import App, Request

from botup import Widget, Context, Dispatcher, Api, Bot, Navigation
from botup.widgets.date_picker import DatePicker
from botup.mixins.echo import EchoMixin
from botup.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "token"
WEBHOOK = f'https://url/{TOKEN}'


class TestMixin:

    def build(self, dispatcher: Dispatcher):
        dispatcher.register_command_handler('/test', self.cmd_test)

    @staticmethod
    async def cmd_test(ctx: Context):
        await ctx.api.send_message(
            chat_id=ctx.chat_id,
            text='Test'
        )


class RootWidget(Widget, TestMixin, EchoMixin):
    async def entry(self, ctx: Context, **kwargs):
        botup_date_picker_result = kwargs.get(DatePicker.DEFAULT_RESULT_KEY)
        if botup_date_picker_result:
            await ctx.api.send_message(
                chat_id=ctx.chat_id,
                text=f'date: {botup_date_picker_result}'
            )
            return

    def build(self, dispatcher: Dispatcher):
        TestMixin.build(self, dispatcher)
        dispatcher.register_command_handler('/start', self.cmd_start)
        dispatcher.register_callback_handler('ready', self.clb_ready)
        EchoMixin.build(self, dispatcher)

    @staticmethod
    async def cmd_start(ctx: Context):
        message = await ctx.api.send_message(
            chat_id=ctx.chat_id,
            text='Click for view date picker',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(callback_data='ready', text='Click')]])
        )
        await ctx.state_manager.set(
            chat_id=ctx.chat_id,
            key='message_id',
            value=str(message.message_id)
        )

    @staticmethod
    async def clb_ready(ctx: Context):
        _, message_id, nav = await gather(
            ctx.api.answer_callback_query(ctx.update.callback_query.id),
            ctx.state_manager.get(
                chat_id=ctx.chat_id,
                key='message_id'
            ),
            Navigation.of(ctx)
        )

        await nav.push(DatePicker.__name__, message_id=int(message_id))


bot = Bot(
    token=TOKEN,
    root=RootWidget(children=[DatePicker()])
)
app = App()


@app.on_event("startup")
async def startup_event():
    async with Api(TOKEN) as api:
        await api.set_webhook(WEBHOOK)


@app.on_event("shutdown")
async def shutdown_event():
    async with Api(TOKEN) as api:
        await api.delete_webhook()

    await bot.close_session()


@app.post(f'/{TOKEN}')
async def index(request: Request):
    await bot.handle(await request.json())
    return ""
```
