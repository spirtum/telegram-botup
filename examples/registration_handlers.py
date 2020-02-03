from botup import Dispatcher
from botup.handlers import CommandHandler, PhotoHandler

dp = Dispatcher()


# Method 1
@dp.command_handler('/start')
def start_handler(chat_id, update):
    pass


# Method 2
dp.register_command_handler('/cancel', start_handler)


# Method 3
dp.register(CommandHandler('/cancel', start_handler))


# or PhotoHandler
def photo_handler(chat_id, update):
    pass
dp.register(PhotoHandler(photo_handler))
