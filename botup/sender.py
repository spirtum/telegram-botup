import os.path
import threading
import time
import uuid
import traceback

import requests

try:
    import ujson as json
except ImportError:
    import json

from .types import ErrorResponse
from .utils import error_response, get_logger, parse_response
from .exceptions import NoTransportException

logger = get_logger()


class TransportMixin:
    FORM_MESSAGE_ID = 'botup:{}:form_message_id'
    LAST_TIME = 'botup:{}:last_time'
    RESULT = 'botup:{}:result'

    def __init__(self, connection):
        self.connection = connection
        if not self.connection:
            self._patch_methods()

    def _patch_methods(self):
        def dummy(*args, **kwargs):
            pass

        self._get_form_message_id = dummy
        self._set_form_message_id = dummy
        self._delete_form_message_id = dummy
        self._set_last_time = dummy
        self._get_last_time = dummy
        self._save_result = dummy
        self._get_result = dummy

    def get_form_message_id(self, chat_id):
        return self.connection.get(self.FORM_MESSAGE_ID.format(chat_id))

    def _set_form_message_id(self, chat_id, value):
        self.connection.set(self.FORM_MESSAGE_ID.format(chat_id), value)

    def _delete_form_message_id(self, chat_id):
        return self.connection.delete(self.FORM_MESSAGE_ID.format(chat_id))

    def _set_last_time(self, chat_id):
        self.connection.set(self.LAST_TIME.format(chat_id), str(time.time()), 10)

    def _get_last_time(self, chat_id):
        return self.connection.get(self.LAST_TIME.format(chat_id))

    def _save_result(self, correlation_id, value):
        self.connection.set(self.RESULT.format(correlation_id), value, 10)

    def _get_result(self, correlation_id):
        value = self.connection.get(self.RESULT.format(correlation_id))
        if not value:
            return
        self.connection.delete(self.RESULT.format(correlation_id))
        return json.loads(value)


class AsyncResult(TransportMixin):
    __slots__ = ['connection', 'correlation_id', '_value']

    def __init__(self, connection, correlation_id):
        super().__init__(connection)
        self.correlation_id = correlation_id
        self._value = None

    def wait(self, timeout=5, parse=True, tick=0.05):
        attempts = timeout // tick
        while not self._value and attempts != 0:
            self._value = self._get_result(self.correlation_id)
            attempts -= 1
            time.sleep(tick)
        if not self._value:
            self._value = {'ok': False, 'error_code': 502, 'description': 'No result'}
        return parse_response(self._value) if parse else self._value


class Sender(TransportMixin):
    API_TIMEOUT = 5
    DEFAULT_QUEUE = 'botup-sender-queue'
    DEFAULT_RATE_LIMIT = 0.5

    def __init__(self, token, connection=None, queue=DEFAULT_QUEUE, rate_limit=DEFAULT_RATE_LIMIT, proxy_string=None):
        super().__init__(connection)
        self.token = token
        self.auto_parse_type = True
        self._queue = queue
        self._rate_limit = rate_limit
        self._url = f'https://api.telegram.org/bot{self.token}/'
        self._req_kwargs = dict(timeout=self.API_TIMEOUT)
        self._set_proxy(proxy_string) if proxy_string else None
        self.functions = {
            self.get_updates.__name__: self.get_updates,
            self.set_webhook.__name__: self.set_webhook,
            self.delete_webhook.__name__: self.delete_webhook,
            self.get_webhook_info.__name__: self.get_webhook_info,
            self.get_me.__name__: self.get_me,
            self.logout.__name__: self.logout,
            self.close.__name__: self.close,
            self.send_message.__name__: self.send_message,
            self.forward_message.__name__: self.forward_message,
            self.copy_message.__name__: self.copy_message,
            self.send_photo.__name__: self.send_photo,
            self.send_audio.__name__: self.send_audio,
            self.send_document.__name__: self.send_document,
            self.send_video.__name__: self.send_video,
            self.send_animation.__name__: self.send_animation,
            self.send_voice.__name__: self.send_voice,
            self.send_video_note.__name__: self.send_video_note,
            self.send_media_group.__name__: self.send_media_group,
            self.send_location.__name__: self.send_location,
            self.edit_message_live_location.__name__: self.edit_message_live_location,
            self.stop_message_live_location.__name__: self.stop_message_live_location,
            self.send_venue.__name__: self.send_venue,
            self.send_contact.__name__: self.send_contact,
            self.send_poll.__name__: self.send_poll,
            self.send_dice.__name__: self.send_dice,
            self.send_chat_action.__name__: self.send_chat_action,
            self.get_user_profile_photos.__name__: self.get_user_profile_photos,
            self.get_file.__name__: self.get_file,
            self.kick_chat_member.__name__: self.kick_chat_member,
            self.unban_chat_member.__name__: self.unban_chat_member,
            self.restrict_chat_member.__name__: self.restrict_chat_member,
            self.promote_chat_member.__name__: self.promote_chat_member,
            self.set_chat_administrator_custom_title.__name__: self.set_chat_administrator_custom_title,
            self.set_chat_permissions.__name__: self.set_chat_permissions,
            self.export_chat_invite_link.__name__: self.export_chat_invite_link,
            self.set_chat_photo.__name__: self.set_chat_photo,
            self.delete_chat_photo.__name__: self.delete_chat_photo,
            self.set_chat_title.__name__: self.set_chat_title,
            self.set_chat_description.__name__: self.set_chat_description,
            self.pin_chat_message.__name__: self.pin_chat_message,
            self.unpin_chat_message.__name__: self.unpin_chat_message,
            self.unpin_all_chat_messages.__name__: self.unpin_all_chat_messages,
            self.leave_chat.__name__: self.leave_chat,
            self.get_chat.__name__: self.get_chat,
            self.get_chat_administrators.__name__: self.get_chat_administrators,
            self.get_chat_members_count.__name__: self.get_chat_members_count,
            self.get_chat_member.__name__: self.get_chat_member,
            self.set_chat_sticker_set.__name__: self.set_chat_sticker_set,
            self.delete_chat_sticker_set.__name__: self.delete_chat_sticker_set,
            self.answer_callback_query.__name__: self.answer_callback_query,
            self.set_my_commands.__name__: self.set_my_commands,
            self.get_my_commands.__name__: self.get_my_commands,
            self.edit_message_text.__name__: self.edit_message_text,
            self.edit_message_caption.__name__: self.edit_message_caption,
            self.edit_message_media.__name__: self.edit_message_media,
            self.edit_message_reply_markup.__name__: self.edit_message_reply_markup,
            self.stop_poll.__name__: self.stop_poll,
            self.delete_message.__name__: self.delete_message,
            self.send_sticker.__name__: self.send_sticker,
            self.get_sticker_set.__name__: self.get_sticker_set,
            self.upload_sticker_file.__name__: self.upload_sticker_file,
            self.create_new_sticker_set.__name__: self.create_new_sticker_set,
            self.add_sticker_to_set.__name__: self.add_sticker_to_set,
            self.set_sticker_position_in_set.__name__: self.set_sticker_position_in_set,
            self.delete_sticker_from_set.__name__: self.delete_sticker_from_set,
            self.set_sticker_set_thumb.__name__: self.set_sticker_set_thumb,
            self.answer_inline_query.__name__: self.answer_inline_query,
            self.send_invoice.__name__: self.send_invoice,
            self.answer_shipping_query.__name__: self.answer_shipping_query,
            self.answer_pre_checkout_query.__name__: self.answer_pre_checkout_query,
            self.set_passport_data_errors.__name__: self.set_passport_data_errors,
            self.send_game.__name__: self.send_game,
            self.set_game_score.__name__: self.set_game_score,
            self.get_game_high_scores.__name__: self.get_game_high_scores
        }

    @classmethod
    def start_new_worker(cls, token, redis_cfg, queue, rate_limit, proxy_string, fake_mode):
        import redis
        instance = cls(
            token=token,
            connection=redis.StrictRedis(**redis_cfg),
            queue=queue,
            rate_limit=rate_limit,
            proxy_string=proxy_string
        )
        instance.auto_parse_type = False
        instance._run_worker(fake_mode)

    def _set_proxy(self, proxy_string):
        if '://' not in proxy_string:
            proxy_string = f'socks5h://{proxy_string}'
        self._req_kwargs['proxies'] = dict(http=proxy_string, https=proxy_string)

    def _delay(self, **kwargs):
        chat_id = kwargs.get('chat_id')
        if not chat_id:
            return 0
        last_time = self._get_last_time(chat_id)
        if not last_time:
            return 0
        time_diff = time.time() - float(last_time)
        return 0 if time_diff > self._rate_limit else self._rate_limit - time_diff

    def _start_task(self, **payload):
        func = payload['func']
        kwargs = payload['kwargs']
        result = self.functions[func](**kwargs)
        self._save_result(payload['correlation_id'], result)
        if payload['save_id'] and 'chat_id' in kwargs:
            data = json.loads(result)
            if not data['ok']:
                return
            if 'message_id' not in data['result']:
                return
            self._set_form_message_id(kwargs['chat_id'], data['result']['message_id'])

    def _run_worker(self, fake_mode=False):
        logger.info('Worker started')
        subscriber = self.connection.pubsub()
        subscriber.subscribe([self._queue])
        for message in subscriber.listen():
            if message['type'] == 'subscribe':
                continue
            payload = json.loads(message['data'])
            if payload['func'] not in self.functions:
                continue
            logger.info('Call {} with {}'.format(payload['func'], payload['kwargs']))
            if fake_mode:
                continue
            timer = threading.Timer(self._delay(**payload['kwargs']), self._start_task, kwargs=payload)
            timer.start()
            timer.join()
            chat_id = payload['kwargs'].get('chat_id')
            self._set_last_time(chat_id) if chat_id else None

    def _error_response(self, text):
        if self.auto_parse_type:
            return ErrorResponse(ok=False, error_code=502, description=text)
        return error_response(text)

    def _request(self, *args, **kwargs):
        try:
            resp = requests.post(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            return self._error_response(f'API connection error. {traceback.format_exc()}')
        except requests.exceptions.Timeout:
            return self._error_response(f'API timeout error. {traceback.format_exc()}')
        return parse_response(resp.text) if self.auto_parse_type else resp.text

    def push(self, func, save_id=False, **kwargs):
        if not self.connection:
            raise NoTransportException('Sender is not connected to transport db')
        correlation_id = str(uuid.uuid4())
        payload = dict(
            func=func.__name__,
            kwargs=kwargs,
            correlation_id=correlation_id,
            save_id=save_id
        )
        self.connection.publish(self._queue, json.dumps(payload))
        return AsyncResult(self.connection, correlation_id)

    def clear(self, chat_id):
        if not self.connection:
            raise NoTransportException('Sender is not connected to transport db')
        message_id = self.get_form_message_id(chat_id)
        if message_id:
            self.push(self.delete_message, chat_id=chat_id, message_id=message_id)
            self._delete_form_message_id(chat_id)
            return True

    def quick_callback_answer(self, update):
        if not self.connection:
            raise NoTransportException('Sender is not connected to transport db')
        assert update.callback_query, 'Update do not have a CallbackQuery'
        self.push(
            func=self.answer_callback_query,
            callback_query_id=update.callback_query.id
        )

    def get_updates(self, offset=None, limit=None, timeout=None, allowed_updates=None):
        return self._request(self._url + 'getUpdates', data=dict(
            offset=offset,
            limit=limit,
            timeout=timeout,
            allowed_updates=allowed_updates), **self._req_kwargs)

    def set_webhook(self,
                    url,
                    certificate=None,
                    ip_address=None,
                    max_connections=None,
                    allowed_updates=None,
                    drop_pending_updates=None):
        kwargs = dict(
            url=url,
            certificate=certificate,
            ip_address=ip_address,
            max_connections=max_connections,
            allowed_updates=allowed_updates,
            drop_pending_updates=drop_pending_updates
        )
        files_kwargs = dict()
        if certificate:
            path = certificate.get('path')
            if not path:
                return self._error_response('Field path in certificate not found')
            if not os.path.isfile(path):
                return self._error_response('File not found')
            files_kwargs['certificate'] = open(path, 'rb')
        return self._request(self._url + 'setWebhook', data=kwargs, files=files_kwargs, **self._req_kwargs)

    def delete_webhook(self, drop_pending_updates=None):
        return self._request(self._url + 'deleteWebhook', data=dict(drop_pending_updates=drop_pending_updates),
                             **self._req_kwargs)

    def get_webhook_info(self):
        return self._request(self._url + 'getWebhookInfo', **self._req_kwargs)

    def get_me(self):
        return self._request(self._url + 'getMe', **self._req_kwargs)

    def logout(self):
        return self._request(self._url + 'logOut', **self._req_kwargs)

    def close(self):
        return self._request(self._url + 'close', **self._req_kwargs)

    def send_message(self,
                     chat_id,
                     text,
                     parse_mode=None,
                     entities=None,
                     disable_web_page_preview=None,
                     disable_notification=None,
                     reply_to_message_id=None,
                     allow_sending_without_reply=None,
                     reply_markup=None):
        return self._request(self._url + 'sendMessage', data=dict(chat_id=chat_id,
                                                                  text=text,
                                                                  parse_mode=parse_mode,
                                                                  entities=entities,
                                                                  disable_web_page_preview=disable_web_page_preview,
                                                                  disable_notification=disable_notification,
                                                                  reply_to_message_id=reply_to_message_id,
                                                                  allow_sending_without_reply=allow_sending_without_reply,
                                                                  reply_markup=reply_markup), **self._req_kwargs)

    def forward_message(self, chat_id, from_chat_id, message_id, disable_notification=None):
        return self._request(self._url + 'forwardMessage', data=dict(chat_id=chat_id,
                                                                     from_chat_id=from_chat_id,
                                                                     message_id=message_id,
                                                                     disable_notification=disable_notification),
                             **self._req_kwargs)

    def copy_message(self,
                     chat_id,
                     from_chat_id,
                     message_id,
                     caption=None,
                     parse_mode=None,
                     caption_entities=None,
                     disable_notification=None,
                     reply_to_message_id=None,
                     allow_sending_without_reply=None,
                     reply_markup=None):
        return self._request(self._url + 'copyMessage', data=dict(
            chat_id=chat_id,
            from_chat_id=from_chat_id,
            message_id=message_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        ), **self._req_kwargs)

    def send_photo(self,
                   chat_id,
                   photo,
                   caption=None,
                   parse_mode=None,
                   disable_notification=None,
                   reply_to_message_id=None,
                   allow_sending_without_reply=None,
                   reply_markup=None):
        kwargs = dict(
            chat_id=chat_id,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )
        files_kwargs = dict()
        file_id = photo.get('file_id')
        url = photo.get('url')
        path = photo.get('path')
        if file_id:
            kwargs['photo'] = file_id
        elif url:
            kwargs['photo'] = url
        elif path:
            if not os.path.isfile(path):
                return self._error_response('File not found')
            files_kwargs['photo'] = open(path, 'rb')
        else:
            return self._error_response('Location not found')
        return self._request(self._url + 'sendPhoto', data=kwargs, files=files_kwargs, **self._req_kwargs)

    def send_audio(self,
                   chat_id,
                   audio,
                   caption=None,
                   parse_mode=None,
                   caption_entities=None,
                   duration=None,
                   performer=None,
                   title=None,
                   thumb=None,
                   disable_notification=None,
                   reply_to_message_id=None,
                   allow_sending_without_reply=None,
                   reply_markup=None):
        kwargs = dict(
            chat_id=chat_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            title=title,
            performer=performer,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )
        files_kwargs = dict()
        file_id = audio.get('file_id')
        url = audio.get('url')
        path = audio.get('path')
        if thumb:
            if not os.path.isfile(thumb):
                return self._error_response('Thumb file not found')
            files_kwargs['thumb'] = open(thumb, 'rb')
        if file_id:
            kwargs['audio'] = file_id
        elif url:
            kwargs['audio'] = url
        elif path:
            if not os.path.isfile(path):
                return self._error_response('File not found')
            files_kwargs['audio'] = open(path, 'rb')
        else:
            return self._error_response('Location not found')
        return self._request(self._url + 'sendAudio', data=kwargs, files=files_kwargs, **self._req_kwargs)

    def send_document(self,
                      chat_id,
                      document,
                      thumb=None,
                      caption=None,
                      parse_mode=None,
                      caption_entities=None,
                      disable_content_type_detection=None,
                      disable_notification=None,
                      reply_to_message_id=None,
                      allow_sending_without_reply=None,
                      reply_markup=None):
        kwargs = dict(
            chat_id=chat_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_content_type_detection=disable_content_type_detection,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )
        files_kwargs = dict()
        file_id = document.get('file_id')
        url = document.get('url')
        path = document.get('path')
        if thumb:
            if not os.path.isfile(thumb):
                return self._error_response('Thumb file not found')
            files_kwargs['thumb'] = open(thumb, 'rb')
        if file_id:
            kwargs['document'] = file_id
        elif url:
            kwargs['document'] = url
        elif path:
            if not os.path.isfile(path):
                return self._error_response('File not found')
            files_kwargs['document'] = open(path, 'rb')
        else:
            return self._error_response('Location not found')
        return self._request(self._url + 'sendDocument', data=kwargs, files=files_kwargs, **self._req_kwargs)

    def send_video(self,
                   chat_id,
                   video,
                   duration=None,
                   width=None,
                   height=None,
                   thumb=None,
                   caption=None,
                   parse_mode=None,
                   caption_entities=None,
                   supports_streaming=None,
                   disable_notification=None,
                   reply_to_message_id=None,
                   allow_sending_without_reply=None,
                   reply_markup=None):
        kwargs = dict(
            chat_id=chat_id,
            duration=duration,
            width=width,
            height=height,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )
        files_kwargs = dict()
        file_id = video.get('file_id')
        url = video.get('url')
        path = video.get('path')
        if thumb:
            if not os.path.isfile(thumb):
                return self._error_response('Thumb file not found')
            files_kwargs['thumb'] = open(thumb, 'rb')
        if file_id:
            kwargs['video'] = file_id
        elif url:
            kwargs['video'] = url
        elif path:
            if not os.path.isfile(path):
                return self._error_response('File not found')
            files_kwargs['video'] = open(path, 'rb')
        else:
            return self._error_response('Location not found')
        return self._request(self._url + 'sendVideo', data=kwargs, files=files_kwargs, **self._req_kwargs)

    def send_animation(self,
                       chat_id,
                       animation,
                       duration=None,
                       width=None,
                       height=None,
                       thumb=None,
                       caption=None,
                       parse_mode=None,
                       caption_entities=None,
                       disable_notification=None,
                       reply_to_message_id=None,
                       allow_sending_without_reply=None,
                       reply_markup=None):
        kwargs = dict(
            chat_id=chat_id,
            duration=duration,
            width=width,
            height=height,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )
        files_kwargs = dict()
        file_id = animation.get('file_id')
        url = animation.get('url')
        path = animation.get('path')
        if thumb:
            if not os.path.isfile(thumb):
                return self._error_response('Thumb file not found')
            files_kwargs['thumb'] = open(thumb, 'rb')
        if file_id:
            kwargs['animation'] = file_id
        elif url:
            kwargs['animation'] = url
        elif path:
            if not os.path.isfile(path):
                return self._error_response('File not found')
            files_kwargs['animation'] = open(path, 'rb')
        else:
            return self._error_response('Location not found')
        return self._request(self._url + 'sendAnimation', data=kwargs, files=files_kwargs, **self._req_kwargs)

    def send_voice(self,
                   chat_id,
                   voice,
                   caption=None,
                   parse_mode=None,
                   caption_entities=None,
                   duration=None,
                   disable_notification=None,
                   reply_to_message_id=None,
                   allow_sending_without_reply=None,
                   reply_markup=None):
        kwargs = dict(
            chat_id=chat_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )
        files_kwargs = dict()
        file_id = voice.get('file_id')
        url = voice.get('url')
        path = voice.get('path')
        if file_id:
            kwargs['voice'] = file_id
        elif url:
            kwargs['voice'] = url
        elif path:
            if not os.path.isfile(path):
                return self._error_response('File not found')
            files_kwargs['voice'] = open(path, 'rb')
        else:
            return self._error_response('Location not found')
        return self._request(self._url + 'sendVoice', data=kwargs, files=files_kwargs, **self._req_kwargs)

    def send_video_note(self,
                        chat_id,
                        video_note,
                        duration=None,
                        length=None,
                        thumb=None,
                        disable_notification=None,
                        reply_to_message_id=None,
                        allow_sending_without_reply=None,
                        reply_markup=None):
        kwargs = dict(
            chat_id=chat_id,
            duration=duration,
            length=length,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup
        )
        files_kwargs = dict()
        file_id = video_note.get('file_id')
        url = video_note.get('url')
        path = video_note.get('path')
        if thumb:
            if not os.path.isfile(thumb):
                return self._error_response('Thumb file not found')
            files_kwargs['thumb'] = open(thumb, 'rb')
        if file_id:
            kwargs['video_note'] = file_id
        elif url:
            kwargs['video_note'] = url
        elif path:
            if not os.path.isfile(path):
                return self._error_response('File not found')
            files_kwargs['video_note'] = open(path, 'rb')
        else:
            return self._error_response('Location not found')
        return self._request(self._url + 'sendVideoNote', data=kwargs, files=files_kwargs, **self._req_kwargs)

    def send_media_group(self,
                         chat_id,
                         media,
                         disable_notification=None,
                         reply_to_message_id=None,
                         allow_sending_without_reply=None):
        kwargs = dict(
            chat_id=chat_id,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply
        )
        kwargs['media'] = list()
        files_kwargs = dict()
        for m in media:
            assert m['type'] in ('photo', 'video'), 'Media must be photo or video'
            if m['media'].startswith('attach://'):
                #  attach://<path/to/file>
                path = m['media'].split('://')[-1]
                files_kwargs[path] = open(path, 'rb')
            kwargs['media'].append(m)
        kwargs['media'] = json.dumps(kwargs['media'])
        return self._request(self._url + 'sendMediaGroup', data=kwargs, files=files_kwargs, **self._req_kwargs)

    def send_location(self,
                      chat_id,
                      latitude,
                      longitude,
                      horizontal_accuracy=None,
                      live_period=None,
                      heading=None,
                      proximity_alert_radius=None,
                      disable_notification=None,
                      reply_to_message_id=None,
                      allow_sending_without_reply=None,
                      reply_markup=None):
        return self._request(self._url + 'sendLocation', data=dict(
            chat_id=chat_id,
            latitude=latitude,
            longitude=longitude,
            horizontal_accuracy=horizontal_accuracy,
            live_period=live_period,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup), **self._req_kwargs)

    def edit_message_live_location(self,
                                   latitude,
                                   longitude,
                                   chat_id=None,
                                   message_id=None,
                                   inline_message_id=None,
                                   horizontal_accuracy=None,
                                   heading=None,
                                   proximity_alert_radius=None,
                                   reply_markup=None):
        return self._request(self._url + 'editMessageLiveLocation', data=dict(
            chat_id=chat_id,
            latitude=latitude,
            longitude=longitude,
            message_id=message_id,
            inline_message_id=inline_message_id,
            horizontal_accuracy=horizontal_accuracy,
            heading=heading,
            proximity_alert_radius=proximity_alert_radius,
            reply_markup=reply_markup), **self._req_kwargs)

    def stop_message_live_location(self, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        return self._request(self._url + 'stopMessageLiveLocation', data=dict(
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            reply_markup=reply_markup), **self._req_kwargs)

    def send_venue(self,
                   chat_id,
                   latitude,
                   longitude,
                   title,
                   address,
                   foursquare_id=None,
                   foursquare_type=None,
                   google_place_id=None,
                   google_place_type=None,
                   disable_notification=None,
                   reply_to_message_id=None,
                   allow_sending_without_reply=None,
                   reply_markup=None):
        return self._request(self._url + 'sendVenue', data=dict(
            chat_id=chat_id,
            latitude=latitude,
            longitude=longitude,
            title=title,
            address=address,
            foursquare_id=foursquare_id,
            foursquare_type=foursquare_type,
            google_place_id=google_place_id,
            google_place_type=google_place_type,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup), **self._req_kwargs)

    def send_contact(self,
                     chat_id,
                     phone_number,
                     first_name,
                     last_name=None,
                     vcard=None,
                     disable_notification=None,
                     reply_to_message_id=None,
                     allow_sending_without_reply=None,
                     reply_markup=None):
        return self._request(self._url + 'sendContact', data=dict(
            chat_id=chat_id,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            vcard=vcard,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup), **self._req_kwargs)

    def send_poll(self,
                  chat_id,
                  question,
                  options,
                  is_anonymous=None,
                  type=None,
                  allows_multiple_answers=None,
                  correct_option_id=None,
                  explanation=None,
                  explanation_parse_mode=None,
                  explanation_entities=None,
                  open_period=None,
                  close_date=None,
                  is_closed=None,
                  disable_notification=None,
                  reply_to_message_id=None,
                  allow_sending_without_reply=None,
                  reply_markup=None):
        if isinstance(options, list):
            options = json.dumps(options)
        return self._request(self._url + 'sendPoll', data=dict(
            chat_id=chat_id,
            question=question,
            options=options,
            is_anonymous=is_anonymous,
            type=type,
            allows_multiple_answers=allows_multiple_answers,
            correct_option_id=correct_option_id,
            explanation=explanation,
            explanation_parse_mode=explanation_parse_mode,
            explanation_entities=explanation_entities,
            open_period=open_period,
            close_date=close_date,
            is_closed=is_closed,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup), **self._req_kwargs)

    def send_dice(self,
                  chat_id,
                  emoji=None,
                  disable_notification=None,
                  reply_to_message_id=None,
                  allow_sending_without_reply=None,
                  reply_markup=None):
        return self._request(self._url + 'sendDice', data=dict(
            chat_id=chat_id,
            emoji=emoji,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup), **self._req_kwargs)

    def send_chat_action(self, chat_id, action):
        return self._request(self._url + 'sendChatAction', data=dict(chat_id=chat_id, action=action),
                             **self._req_kwargs)

    def get_user_profile_photos(self, user_id, offset=None, limit=None):
        return self._request(self._url + 'getUserProfilePhotos', data=dict(
            user_id=user_id, offset=offset, limit=limit), **self._req_kwargs)

    def get_file(self, file_id):
        return self._request(self._url + 'getFile', data=dict(file_id=file_id), **self._req_kwargs)

    def kick_chat_member(self, chat_id, user_id, until_date=None):
        return self._request(self._url + 'kickChatMember', data=dict(
            chat_id=chat_id, user_id=user_id, until_date=until_date), **self._req_kwargs)

    def unban_chat_member(self, chat_id, user_id, only_if_banned=None):
        return self._request(self._url + 'unbanChatMember', data=dict(
            chat_id=chat_id,
            user_id=user_id,
            only_if_banned=only_if_banned), **self._req_kwargs)

    def restrict_chat_member(self, chat_id, user_id, permissions, until_date=None):
        return self._request(self._url + 'restrictChatMember', data=dict(
            chat_id=chat_id,
            user_id=user_id,
            permissions=permissions,
            until_date=until_date
        ), **self._req_kwargs)

    def promote_chat_member(self,
                            chat_id,
                            user_id,
                            is_anonymous=None,
                            can_change_info=None,
                            can_post_messages=None,
                            can_edit_messages=None,
                            can_delete_messages=None,
                            can_invite_users=None,
                            can_restrict_members=None,
                            can_pin_messages=None,
                            can_promote_members=None):
        return self._request(self._url + 'promoteChatMember', data=dict(
            chat_id=chat_id,
            user_id=user_id,
            is_anonymous=is_anonymous,
            can_change_info=can_change_info,
            can_post_messages=can_post_messages,
            can_edit_messages=can_edit_messages,
            can_delete_messages=can_delete_messages,
            can_invite_users=can_invite_users,
            can_restrict_members=can_restrict_members,
            can_pin_messages=can_pin_messages,
            can_promote_members=can_promote_members), **self._req_kwargs)

    def set_chat_administrator_custom_title(self, chat_id, user_id, custom_title):
        return self._request(self._url + 'setChatAdministratorCustomTitle', data=dict(
            chat_id=chat_id,
            user_id=user_id,
            custom_title=custom_title), **self._req_kwargs)

    def set_chat_permissions(self, chat_id, permissions):
        return self._request(self._url + 'setChatPermissions', data=dict(
            chat_id=chat_id,
            permissions=permissions), **self._req_kwargs)

    def export_chat_invite_link(self, chat_id):
        return self._request(self._url + 'exportChatInviteLink', data=dict(chat_id=chat_id), **self._req_kwargs)

    def set_chat_photo(self, chat_id, photo):
        kwargs = dict(chat_id=chat_id)
        files_kwargs = dict()
        file_id = photo.get('file_id')
        url = photo.get('url')
        path = photo.get('path')
        if file_id:
            kwargs['photo'] = file_id
        elif url:
            kwargs['photo'] = url
        elif path:
            if not os.path.isfile(path):
                return self._error_response('File not found')
            files_kwargs['photo'] = open(path, 'rb')
        else:
            return self._error_response('Location not found')
        return self._request(self._url + 'setChatPhoto', data=kwargs, files=files_kwargs, **self._req_kwargs)

    def delete_chat_photo(self, chat_id):
        return self._request(self._url + 'deleteChatPhoto', data=dict(chat_id=chat_id), **self._req_kwargs)

    def set_chat_title(self, chat_id, title):
        return self._request(self._url + 'setChatTitle', data=dict(chat_id=chat_id, title=title), **self._req_kwargs)

    def set_chat_description(self, chat_id, description=None):
        return self._request(self._url + 'setChatDescription', data=dict(chat_id=chat_id, description=description),
                             **self._req_kwargs)

    def pin_chat_message(self, chat_id, message_id, disable_notification=None):
        return self._request(self._url + 'pinChatMessage', data=dict(
            chat_id=chat_id, message_id=message_id, disable_notification=disable_notification), **self._req_kwargs)

    def unpin_chat_message(self, chat_id, message_id=None):
        return self._request(self._url + 'unpinChatMessage', data=dict(
            chat_id=chat_id,
            message_id=message_id), **self._req_kwargs)

    def unpin_all_chat_messages(self, chat_id):
        return self._request(self._url + 'unpinAllChatMessages', data=dict(chat_id=chat_id), **self._req_kwargs)

    def leave_chat(self, chat_id):
        return self._request(self._url + 'leaveChat', data=dict(chat_id=chat_id), **self._req_kwargs)

    def get_chat(self, chat_id):
        return self._request(self._url + 'getChat', data=dict(chat_id=chat_id), **self._req_kwargs)

    def get_chat_administrators(self, chat_id):
        return self._request(self._url + 'getChatAdministrators', data=dict(chat_id=chat_id), **self._req_kwargs)

    def get_chat_members_count(self, chat_id):
        return self._request(self._url + 'getChatMembersCount', data=dict(chat_id=chat_id), **self._req_kwargs)

    def get_chat_member(self, chat_id, user_id):
        return self._request(self._url + 'getChatMember', data=dict(chat_id=chat_id, user_id=user_id),
                             **self._req_kwargs)

    def set_chat_sticker_set(self, chat_id, sticker_set_name):
        return self._request(self._url + 'setChatStickerSet',
                             data=dict(chat_id=chat_id, sticker_set_name=sticker_set_name), **self._req_kwargs)

    def delete_chat_sticker_set(self, chat_id):
        return self._request(self._url + 'deleteChatStickerSet', data=dict(chat_id=chat_id), **self._req_kwargs)

    def answer_callback_query(self,
                              callback_query_id,
                              text=None,
                              show_alert=None,
                              url=None,
                              cache_time=None):
        return self._request(self._url + 'answerCallbackQuery', data=dict(
            callback_query_id=callback_query_id,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time), **self._req_kwargs)

    def set_my_commands(self, commands):
        return self._request(self._url + 'setMyCommands', data=dict(commands=json.dumps(commands)), **self._req_kwargs)

    def get_my_commands(self):
        return self._request(self._url + 'getMyCommands', **self._req_kwargs)

    def edit_message_text(self,
                          text,
                          chat_id=None,
                          message_id=None,
                          inline_message_id=None,
                          parse_mode=None,
                          entities=None,
                          disable_web_page_preview=None,
                          reply_markup=None):
        return self._request(self._url + 'editMessageText', data=dict(
            text=text,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup), **self._req_kwargs)

    def edit_message_caption(self,
                             chat_id=None,
                             message_id=None,
                             inline_message_id=None,
                             caption=None,
                             parse_mode=None,
                             caption_entities=None,
                             reply_markup=None):
        return self._request(self._url + 'editMessageCaption', data=dict(
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            reply_markup=reply_markup), **self._req_kwargs)

    def edit_message_media(self, media, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        return self._request(self._url + 'editMessageMedia', data=dict(
            media=media,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            reply_markup=reply_markup), **self._req_kwargs)

    def edit_message_reply_markup(self, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        return self._request(self._url + 'editMessageReplyMarkup', data=dict(
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            reply_markup=reply_markup), **self._req_kwargs)

    def stop_poll(self, chat_id, message_id, reply_markup=None):
        return self._request(self._url + 'stopPoll', data=dict(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup), **self._req_kwargs)

    def delete_message(self, chat_id, message_id):
        return self._request(self._url + 'deleteMessage', data=dict(chat_id=chat_id, message_id=message_id),
                             **self._req_kwargs)

    def send_sticker(self,
                     chat_id,
                     sticker,
                     disable_notification=None,
                     reply_to_message_id=None,
                     allow_sending_without_reply=None,
                     reply_markup=None):
        kwargs = dict(
            chat_id=chat_id,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup)
        files_kwargs = dict()
        file_id = sticker.get('file_id')
        url = sticker.get('url')
        path = sticker.get('path')
        if file_id:
            kwargs['sticker'] = file_id
        elif url:
            kwargs['sticker'] = url
        elif path:
            if not os.path.isfile(path):
                return self._error_response('File not found')
            files_kwargs['sticker'] = open(path, 'rb')
        else:
            return self._error_response('Location not found')
        return self._request(self._url + 'sendSticker', data=kwargs, files=files_kwargs, **self._req_kwargs)

    def get_sticker_set(self, name):
        return self._request(self._url + 'getStickerSet', data=dict(name=name), **self._req_kwargs)

    def upload_sticker_file(self, user_id, png_sticker):
        kwargs = dict(user_id=user_id)
        files_kwargs = dict()
        file_id = png_sticker.get('file_id')
        url = png_sticker.get('url')
        path = png_sticker.get('path')
        if file_id:
            kwargs['png_sticker'] = file_id
        elif url:
            kwargs['png_sticker'] = url
        elif path:
            if not os.path.isfile(path):
                return self._error_response('File not found')
            files_kwargs['png_sticker'] = open(path, 'rb')
        else:
            return self._error_response('Location not found')
        return self._request(self._url + 'uploadStickerFile', data=kwargs, files=files_kwargs, **self._req_kwargs)

    def create_new_sticker_set(self,
                               user_id,
                               name,
                               title,
                               emojis,
                               png_sticker=None,
                               tgs_sticker=None,
                               contains_masks=None,
                               mask_position=None):
        if png_sticker and tgs_sticker:
            return self._error_response('You must use exactly one of the fields png_sticker or tgs_sticker')
        kwargs = dict(user_id=user_id, name=name, title=title, emojis=emojis, contains_masks=contains_masks)
        files_kwargs = dict()
        sticker, sticker_key = (png_sticker, 'png_sticker') if png_sticker else (tgs_sticker, 'tgs_sticker')
        file_id = sticker.get('file_id')
        url = sticker.get('url')
        path = sticker.get('path')
        if file_id:
            kwargs[sticker_key] = file_id
        elif url:
            kwargs[sticker_key] = url
        elif path:
            if not os.path.isfile(path):
                return self._error_response('File not found')
            files_kwargs[sticker_key] = open(path, 'rb')
        else:
            return self._error_response('Location not found')
        if contains_masks:
            kwargs['mask_position'] = json.dumps(mask_position)
        return self._request(self._url + 'createNewStickerSet', data=kwargs, files_kwargs=files_kwargs,
                             **self._req_kwargs)

    def add_sticker_to_set(self, user_id, name, emojis, png_sticker=None, tgs_sticker=None, mask_position=None):
        if png_sticker and tgs_sticker:
            return self._error_response('You must use exactly one of the fields png_sticker or tgs_sticker')
        kwargs = dict(user_id=user_id, name=name, emojis=emojis)
        files_kwargs = dict()
        sticker, sticker_key = (png_sticker, 'png_sticker') if png_sticker else (tgs_sticker, 'tgs_sticker')
        file_id = sticker.get('file_id')
        url = sticker.get('url')
        path = sticker.get('path')
        if file_id:
            kwargs[sticker_key] = file_id
        elif url:
            kwargs[sticker_key] = url
        elif path:
            if not os.path.isfile(path):
                return self._error_response('File not found')
            files_kwargs[sticker_key] = open(path, 'rb')
        else:
            return self._error_response('Location not found')
        if mask_position:
            kwargs['mask_position'] = json.dumps(mask_position)
        return self._request(self._url + 'addStickerToSet', data=kwargs, files_kwargs=files_kwargs, **self._req_kwargs)

    def set_sticker_position_in_set(self, sticker, position):
        return self._request(self._url + 'setStickerPositionInSet', data=dict(sticker=sticker, position=position),
                             **self._req_kwargs)

    def delete_sticker_from_set(self, sticker):
        return self._request(self._url + 'deleteStickerFromSet', data=dict(sticker=sticker), **self._req_kwargs)

    def set_sticker_set_thumb(self, name, user_id, thumb):
        kwargs = dict(name=name, user_id=user_id)
        files_kwargs = dict()
        file_id = thumb.get('file_id')
        url = thumb.get('url')
        path = thumb.get('path')
        if file_id:
            kwargs['thumb'] = file_id
        elif url:
            kwargs['thumb'] = url
        elif path:
            if not os.path.isfile(path):
                return self._error_response('File not found')
            files_kwargs['thumb'] = open(path, 'rb')
        else:
            return self._error_response('Location not found')
        return self._request(self._url + 'setStickerSetThumb', data=kwargs, files_kwargs=files_kwargs,
                             **self._req_kwargs)

    def answer_inline_query(self,
                            inline_query_id,
                            results,
                            cache_time=None,
                            is_personal=None,
                            next_offset=None,
                            switch_pm_text=None,
                            switch_pm_parameter=None):
        return self._request(self._url + 'answerInlineQuery', data=dict(
            inline_query_id=inline_query_id,
            results=json.dumps(results),
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter=switch_pm_parameter), **self._req_kwargs)

    def send_invoice(self,
                     chat_id,
                     title,
                     description,
                     payload,
                     provider_token,
                     start_parameter,
                     currency,
                     prices,
                     provider_data=None,
                     photo_url=None,
                     photo_size=None,
                     photo_width=None,
                     photo_height=None,
                     need_name=None,
                     need_phone_number=None,
                     need_email=None,
                     need_shipping_address=None,
                     send_phone_number_to_provider=None,
                     send_email_to_provider=None,
                     is_flexible=None,
                     disable_notification=None,
                     reply_to_message_id=None,
                     allow_sending_without_reply=None,
                     reply_markup=None):
        return self._request(self._url + 'sendInvoice', data=dict(
            chat_id=chat_id,
            title=title,
            description=description,
            payload=payload,
            provider_token=provider_token,
            start_parameter=start_parameter,
            currency=currency, prices=prices,
            provider_data=provider_data,
            photo_url=photo_url,
            photo_size=photo_size,
            photo_width=photo_width,
            photo_height=photo_height,
            need_name=need_name,
            need_phone_number=need_phone_number,
            need_email=need_email,
            need_shipping_address=need_shipping_address,
            send_phone_number_to_provider=send_phone_number_to_provider,
            send_email_to_provider=send_email_to_provider,
            is_flexible=is_flexible,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup), **self._req_kwargs)

    def answer_shipping_query(self, shipping_query_id, ok, shipping_options=None, error_message=None):
        return self._request(self._url + 'answerShippingQuery', data=dict(
            shipping_query_id=shipping_query_id,
            ok=ok,
            shipping_options=shipping_options,
            error_message=error_message), **self._req_kwargs)

    def answer_pre_checkout_query(self, pre_checkout_query_id, ok, error_message=None):
        return self._request(self._url + 'answerPreCheckoutQuery', data=dict(
            pre_checkout_query_id=pre_checkout_query_id,
            ok=ok,
            error_message=error_message), **self._req_kwargs)

    def set_passport_data_errors(self, user_id, errors):
        return self._request(self._url + 'setPassportDataErrors', data=dict(user_id=user_id, errors=errors),
                             **self._req_kwargs)

    def send_game(self,
                  chat_id,
                  game_short_name,
                  disable_notification=None,
                  reply_to_message_id=None,
                  allow_sending_without_reply=None,
                  reply_markup=None):
        return self._request(self._url + 'sendGame', data=dict(
            chat_id=chat_id,
            game_short_name=game_short_name,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup), **self._req_kwargs)

    def set_game_score(self,
                       user_id,
                       score,
                       force=None,
                       disable_edit_message=None,
                       chat_id=None,
                       message_id=None,
                       inline_message_id=None):
        return self._request(self._url + 'setGameScore', data=dict(
            user_id=user_id,
            score=score,
            force=force,
            disable_edit_message=disable_edit_message,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id), **self._req_kwargs)

    def get_game_high_scores(self, user_id, chat_id=None, message_id=None, inline_message_id=None):
        return self._request(self._url + 'getGameHighScores', data=dict(
            user_id=user_id,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id), **self._req_kwargs)
