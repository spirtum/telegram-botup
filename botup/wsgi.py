import os
import re
import multiprocessing
import traceback
import pprint

from flask import Flask, request

from . import dispatcher, types, handlers, utils
from .sender import Sender
from .exceptions import ConfigException

log = utils.get_logger()
keyboard_types = (
    types.ReplyKeyboardMarkup,
    types.ReplyKeyboardRemove,
    types.InlineKeyboardMarkup
)


class WSGIApp(Flask):

    def __init__(self, *args, **kwargs):
        dp = kwargs.pop('botup_dispatcher')
        token = kwargs.pop('botup_token')
        super().__init__(*args, **kwargs)

        def index():
            try:
                dp.handle(request.get_json())
            except:
                print(traceback.format_exc())
            return "!", 200

        self.add_url_rule(f'/{token}', view_func=index, methods=["POST"])

    @classmethod
    def from_yaml_file(cls, path=None):
        import yaml
        import redis
        utils.setup_logging()
        path = path or os.getenv('BOTUP_YAML_FILE')
        data = yaml.safe_load(open(path, 'r'))
        config = data['config']
        rdb = None
        if config.get('redis'):
            config['redis']['decode_responses'] = True
            config['redis']['encoding'] = 'utf-8'
            rdb = redis.StrictRedis(**config['redis'])
        sn = Sender(
            token=config['token'],
            connection=rdb,
            proxy_string=config.get('proxy_string')
        )

        if config.get('async') and not config.get('redis'):
            raise ConfigException('Cannot use async mod without redis')

        if not rdb and data['entrypoint']['type'] == 'StateDispatcher':
            raise ConfigException('Cannot use StateDispatcher without redis')

        sm = dispatcher.StateManager(rdb)
        dp = DispatcherFactory(sn, sm, data['entrypoint'], config)

        if config.get('webhook_auto_setup'):
            log.info(f'Setup webhook for {config["webhook_url"]}')
            response = sn.set_webhook(f'{config["webhook_url"]}/{config["token"]}')
            if response.is_error():
                raise Exception(response.description)
            else:
                log.info(response.description)

        if config.get('async'):
            log.info(f'Run worker with config:\n{pprint.pformat(config)}')
            run_worker(config)

        return cls(
            __name__,
            botup_dispatcher=dp,
            botup_token=config['token']
        )


def HandlerFactory(sn, sm, function, async_mode, kwargs, states):
    for k, v in kwargs.items():
        if isinstance(v, str):
            continue
        v_type = getattr(types, v['type'])
        v_new = v_type(**v.get('kwargs', {}))
        kwargs[k] = v_new.as_json() if v_type in keyboard_types else v_new.as_dict()
    api_method = getattr(sn, function)
    if async_mode:
        kwargs['func'] = api_method
        method = getattr(sn, 'push')
    else:
        method = api_method

    def handler(chat_id, update):
        local_kwargs = kwargs.copy()
        local_kwargs['chat_id'] = chat_id
        if states:
            for key, value in states.items():
                if value == 'reset':
                    sm.reset(key)
                    continue
                sm.set(key, value)
        method(**local_kwargs)
    return handler


def DispatcherFactory(sn, sm, data, config):
    DispatcherType = getattr(dispatcher, data['type'])
    key = data.get('key', '_')
    args = (sm, data['key']) if DispatcherType is dispatcher.StateDispatcher else ()
    dp = DispatcherType(*args)
    for handler_type, handlers_data in data.get('handlers', {}).items():
        Handler = getattr(handlers, handler_type)
        for hd in handlers_data:
            handler = HandlerFactory(
                sn=sn,
                sm=sm,
                function=hd['function'],
                async_mode=config.get('async'),
                kwargs=hd['kwargs'],
                states=hd.get('states')
            )
            args = (handler,)
            if 'pattern' in hd:
                pattern = hd['pattern']
                if hd.get('regexp'):
                    pattern = re.compile(pattern)
                args = (pattern, handler)
            dp.register(Handler(*args))
            log.info(f'[{key}] Register {Handler.__name__}({hd.get("pattern")}).'
                     f'{hd["function"]}{hd["kwargs"]}')
    for data in data.get('children', []):
        dp.register_state(data['key'], DispatcherFactory(sn, sm, data, config))
        log.info(f'[{key}] Register child "{data["key"]}"')
    return dp


def run_worker(config):
    import redis
    sn = Sender(
        token=config['token'],
        connection=redis.StrictRedis(**config['redis']),
        proxy_string=config.get('proxy_string')
    )
    sn.auto_parse_type = False
    process = multiprocessing.Process(
        target=sn._run_worker,
        args=(False,)
    )
    process.start()
    return process.pid


app = None
if os.environ.get('BOTUP_YAML_FILE'):
    app = WSGIApp.from_yaml_file()
