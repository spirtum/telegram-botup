# Telegram-botup


## Installation
```
$ pip install telegram-botup
```

## Example
```python
# app.py

from botup import Dispatcher, Sender
from some_web_library import App

TOKEN = "token"

sender = Sender(TOKEN)
dispatcher = Dispatcher()

app = App()

@dispatcher.message_handler('hello')
async def hello_handler(chat_id, update):
    await sender.send_message(chat_id, f'Hello {update.message.from_.first_name}')
    

@app.post(f'/{TOKEN}')
async def index(request):
    await dispatcher.handle(await request.json())
    return "ok"
```
