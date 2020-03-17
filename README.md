# Telegram-botup

The library has several utilities for creating telegram bots:

- **Dispatcher** handles incoming updates
- **Sender** implements Telegram API methods
- Other utils, types and etc


## Installation
```
$ pip install telegram-botup
```

## Example
```
$ pip install telegram-botup flask
```

```
# app.py

from botup import Dispatcher, Sender
from botup.wsgi import WSGIApp  # using Flask

TOKEN = "token"

sender = Sender(TOKEN)
dispatcher = Dispatcher()
app = WSGIApp(__name__, botup_dispatcher=dispatcher, botup_token=TOKEN)


@dispatcher.message_handler('hello')
def hello_handler(chat_id, update):
    sender.send_message(chat_id, f'Hello {update.message.from_.first_name}')
```
```
$ flask run
```

## AutoStart Example
```
# botup.yml

config:
  token: "token"
  webhook_url: "https://webhook.example.com"
  proxy_string: "socks5h://localhost:3333"
  webhook_auto_setup: True

entrypoint:
  type: Dispatcher
  key: main
  handlers:
    CommandHandler:
      - pattern: /start
        function: send_message
        kwargs:
          text: "Hello"
```
```
$ botup start
```

### send_photo
```
- pattern: /photo
    function: send_photo
    kwargs:
      photo:
        type: InputFile
        kwargs:
          path: /home/dshebo/Downloads/cat.jpeg
```

### keyboard
```
- pattern: /kb
    function: send_message
    kwargs:
      text: "keyboard\n/remove"
      reply_markup:
        type: ReplyKeyboardMarkup
        kwargs:
          keyboard:
            - - text: 1
              - text: 2
              - text: 3
            - - text: 4
              - text: 5
              - text: 6
          resize_keyboard: True
  - pattern: /remove
    function: send_message
    kwargs:
      text: removed
      reply_markup:
        type: ReplyKeyboardRemove
```

### states
```
config:
  token: "token"
  webhook_url: "https://webhook.example.com"
  proxy_string: "socks5h://localhost:3333"
  webhook_auto_setup: True
  redis:
    host: "localhost"
    port: 6379
    db: 0

entrypoint:
  type: StateDispatcher
  key: main
  handlers:
    CommandHandler:
      - pattern: /start
        function: send_message
        kwargs:
          text: "For change state click below command\n/change\n\nFor print current state click command\n/print"
      - pattern: /print
        function: send_message
        kwargs:
          text: "state = main"
      - pattern: /change
        states:
          main: changed
        function: send_message
        kwargs:
          text: "For return press\n/back\n\nFor print current state click command\n/print"
  children:
    - type: Dispatcher
      key: changed
      handlers:
        CommandHandler:
          - pattern: /print
            function: send_message
            kwargs:
              text: "state = changed"
          - pattern: /back
            states:
              main: reset
            function: send_message
            kwargs:
              text: "Return to default\n/start"
```

