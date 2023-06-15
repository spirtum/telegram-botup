import re

from botup.dispatcher import Dispatcher
from botup.widget import Context


class EchoMixin:

    def build(self, dispatcher: Dispatcher):
        dispatcher.register_message_handler(re.compile(r'.*'), self.msg_echo)

    @staticmethod
    async def msg_echo(ctx: Context):
        await ctx.api.send_message(
            chat_id=ctx.chat_id,
            text=ctx.update.message.text
        )
