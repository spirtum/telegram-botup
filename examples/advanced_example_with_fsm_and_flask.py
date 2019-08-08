from flask import Flask, request
from botup import Bot, Form
from botup.utils import FSM
from botup.types.common import InlineKeyboardMarkup

from config import TOKEN, redis_connection


app = Flask(__name__)
bot = Bot()
form = Form(token=TOKEN, connection=redis_connection)


class MyFSM(FSM):
    KEY = 'user:{}:state'
    STATES = ['start', 'help_page', 'about_form', 'new_user_nickname']


fsm = MyFSM(connection=redis_connection)


def start_handler(chat_id, update):
    fsm.set(chat_id, fsm.start)
    k = InlineKeyboardMarkup()
    k.line(k.callback_data('Set user nickname', 'set_user_nickname'))
    k.line(k.url('About bot', 'https://some-external-url'))
    form.push(
        func=form.send_message,
        chat_id=chat_id,
        text='Hello, do you want set your nickname for this bot?',
        reply_markup=k.as_dict()
    )


def help_handler(chat_id, update):
    fsm.set(chat_id, fsm.help_page)
    text = str()
    text += "Help page:\n\n"
    text += "/start - to start\n"
    text += "/help - to show this message again\n"
    form.push(
        func=form.send_message,
        chat_id=chat_id,
        text=text
    )


def send_new_user_nickname_form(chat_id, update):
    form.quick_callback_answer(update)
    fsm.set(chat_id, fsm.new_user_nickname)
    form.push(
        func=form.send_message,
        chat_id=chat_id,
        text='Enter new your nickname'
    )


def universal_message_handler(chat_id, update):
    fsm.fetch(chat_id)
    if fsm.state == fsm.new_user_nickname:
        #  [*] Saving nickname from update.message.text and redirecting to start form
        start_handler(chat_id, update)
    else:
        form.push(
            func=form.send_message,
            chat_id=chat_id,
            text='Oops, redirecting to start'
        )
        start_handler(chat_id, update)


# Command handlers
bot.register_command_handler('/start', start_handler)
bot.register_command_handler('/help', help_handler)
bot.register_command_handler('*', help_handler)

# Message handlers
bot.register_message_handler('*', universal_message_handler)

# Callback handlers
bot.register_callback_handler('set_user_nickname', send_new_user_nickname_form)


@app.route(f'/{TOKEN}', methods=['POST'])
def index():
    # Receive incoming update from Telegram API using webhook
    try:
        req = request.get_json()
        bot.handle(req)
    except Exception as exc:
        import traceback
        print(traceback.format_exc())
    return "!", 200
