from typing import List

from fastapi import FastAPI, Request

from botup import Widget, Context, Bot, Navigation, Dispatcher, Api
from botup.widgets.date_picker import DatePicker

TOKEN = ""
WEBHOOK = f'https:///{TOKEN}'

app = FastAPI(docs_url=None, redoc_url=None)


class RootWidget(Widget):
    """
    Type "go" message
    """

    KEY = 'root'
    DATE_PICKER_KEY = 'date_picker'

    async def entry(self, ctx: Context, *args, **kwargs):
        botup_date_picker_result = kwargs.get('botup_date_picker_result')
        if botup_date_picker_result:
            await ctx.api.send_message(
                chat_id=ctx.chat_id,
                text=f'date: {botup_date_picker_result}'
            )

    def build(self, dispatcher: Dispatcher):
        dispatcher.register_message_handler('go', self.go_handler)

    @staticmethod
    async def go_handler(ctx: Context):
        nav = await Navigation.of(ctx)
        await nav.push('date_picker')


root_widget = RootWidget(
    key=RootWidget.KEY,
    children=[
        DatePicker(RootWidget.DATE_PICKER_KEY)
    ]
)

bot = Bot(
    token=TOKEN,
    root_widget=root_widget
)


@app.on_event("startup")
async def startup_event():
    api = Api(TOKEN)
    response = await api.set_webhook(WEBHOOK)
    print(response)
    await api.close_session()


@app.on_event("shutdown")
async def shutdown_event():
    api = Api(TOKEN)
    response = await api.delete_webhook()
    print(response)
    await api.close_session()


@app.post(f'/{TOKEN}')
async def index(request: Request):
    await bot.handle(await request.json())
    return {'ok': True}
