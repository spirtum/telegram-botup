# Telegram-botup

Library for fast development and simple deployment of Telegram bots. She includes four basic component:

- **Bot** for handlers registration and receiving incoming updates
- **Form** for working with Telegram API
- **Sender**-worker for asynchronus requests
- Other utils, types and etc

# Features

- Full support of types and methods telegram API
- Built-in **Sender**-worker for making requests like task by task
- Simple switching between synchronus and asynchronus work
- Simple deployment with wsgi
- Built-in command-line tool
- Support of work with socks5-proxy and proxy-url

# Components
## Bot

**Bot** handles incoming updates from Telegram API and invokes user handlers. He has two work mode, with webhook and long-polling:

- Webhook
```
bot.handle(request)
```
- Long-polling
```
bot.polling(*args, **kwargs)
```

## Form

**Form** works in one of two modes: Synchronus and asynchronus

1. *Synchronus*. Simple usage

- Direct invoke API methods
- Requests block runtime
- Blocking from Telegram API is possible

```
form = Form(token=TOKEN)
resp = form.send_message(**kwargs)
```

2. *Asynchronus*. Advanced usage

- Runtime no blocking
- Form send task to **Sender**-worker instead direct request to Telegram API
- **Sender**-worker regulates requests per seconds
- Production ready!

```
form = Form(token=TOKEN, connection=REDIS_CONNECTION)
form.push(form.send_message, **kwargs)
```

For getting response from Telegram API in asynchronus mode use a *wait()*:
```
resp = form.push(form.send_message, **kwargs).wait()
```

## Sender-worker

**Sender** works in another proccess and receives tasks using a **Redis**. For start **Sender** needs token and redis-connection credentials. For more information:

```
$ botup run_sender --help
```

## Other. CLI

```
$ botup --help
```


# Installation
```
$ pip install git+https://bitbucket.org/dimashebo/telegram-botup
```

# Simple example. Using a long-polling and sync-mode without Redis
```
from botup import Bot, Form

TOKEN = '<TOKEN>'

bot = Bot()
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


bot.register_command_handler('/help', help_handler)
bot.register_command_handler('/start', start_handler)


if __name__ == '__main__':
    bot.polling(form)
```

## Q/A

* *How to set webhook?*

```
$ botup set_webhook --help
```

* *How to test bot without requests?*


Use **fake_mode=True** on **Form** initialization

```
form = Form(..., fake_mode=True, ...)
```

Or use **--fake-mode** on **Sender** starting

```
$ botup run_sender --token $TOKEN --fake-mode
```