from botup import Dispatcher, Form

TOKEN = '<TOKEN>'

dispatcher = Dispatcher()
form = Form(token=TOKEN)


def start_handler(chat_id, update):
    form.send_message(
        chat_id=chat_id,
        text='Start handler'
    )


def help_handler(chat_id, update):
    text = str()
    text += "Help page:\n\n"
    text += "/start - to start\n"
    text += "/help - to show this message again\n"
    form.send_message(
        chat_id=chat_id,
        text=text
        )


dispatcher.register_command_handler('/help', help_handler)
dispatcher.register_command_handler('/start', start_handler)


if __name__ == '__main__':
    dispatcher.polling(form)
