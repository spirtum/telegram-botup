from flask import Flask, request
from botup import Dispatcher, Sender

TOKEN = "token"

flask_app = Flask(__name__)
dispatcher = Dispatcher()
sender = Sender(TOKEN)


@dispatcher.message_handler('hello')
def hello_handler(chat_id, update):
    sender.send_message(chat_id, f'Hello {update.message.from_.first_name}')


@flask_app.route(f'/{TOKEN}', methods=['POST'])
def index():
    dispatcher.handle(request.get_json())
    return "!", 200
