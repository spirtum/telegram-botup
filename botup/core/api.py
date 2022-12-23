import os.path
import traceback

from aiohttp import ClientSession, ClientError

try:
    import ujson as json
except ImportError:
    import json

from .types import ErrorResponse, TelegramResponse
from .utils import get_logger

logger = get_logger()


class Api:
    TIMEOUT = 5

    def __init__(self, token, auto_parse_type=True):
        self._message_id_data = {}
        self._token = token
        self._auto_parse_type = auto_parse_type
        self._url = f'https://api.telegram.org/bot{self._token}/'
        self._session = ClientSession()

    async def close_session(self):
        await self._session.close()

    def get_form_message_id(self, chat_id):
        return self._message_id_data.get(chat_id)

    def _set_form_message_id(self, chat_id, value):
        self._message_id_data[chat_id] = value

    def _delete_form_message_id(self, chat_id):
        value = self._message_id_data.get(chat_id)
        if not value:
            return
        del self._message_id_data[chat_id]
        return value

    async def wait_for_message_id(self, chat_id, future):
        result = await future
        message_id = getattr(result, 'message_id', None)
        if not message_id:
            return
        self._set_form_message_id(chat_id, message_id)
        return message_id

    def _error_response(self, text):
        if self._auto_parse_type:
            return ErrorResponse(ok=False, error_code=502, description=text)
        return json.dumps({'ok': False, 'error_code': 502, 'description': text})

    async def _request(self, *args, **kwargs):
        try:
            resp = await self._session.post(*args, **kwargs)
        except ClientError:
            return self._error_response(f'API error:\n{traceback.format_exc()}')
        return TelegramResponse(await resp.json()) if self._auto_parse_type else resp.text

    async def clear(self, chat_id):
        message_id = self.get_form_message_id(chat_id)
        if message_id:
            await self.delete_message(chat_id=chat_id, message_id=message_id)
            self._delete_form_message_id(chat_id)
            return True

    async def quick_callback_answer(self, update):
        if not update.callback_query:
            return
        await self.answer_callback_query(callback_query_id=update.callback_query.id)

    async def get_updates(self, offset=None, limit=None, timeout=None, allowed_updates=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'getUpdates', data=data, timeout=self.TIMEOUT)

    async def set_webhook(self,
                          url,
                          ip_address=None,
                          max_connections=None,
                          allowed_updates=None,
                          drop_pending_updates=None):

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'setWebhook', data=data, timeout=self.TIMEOUT)

    async def delete_webhook(self, drop_pending_updates=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(
            self._url + 'deleteWebhook',
            data=data,
            timeout=self.TIMEOUT
        )

    async def get_webhook_info(self):
        return await self._request(self._url + 'getWebhookInfo', timeout=self.TIMEOUT)

    async def get_me(self):
        return await self._request(self._url + 'getMe', timeout=self.TIMEOUT)

    async def logout(self):
        return await self._request(self._url + 'logOut', timeout=self.TIMEOUT)

    async def close(self):
        return await self._request(self._url + 'close', timeout=self.TIMEOUT)

    async def send_message(self,
                           chat_id,
                           text,
                           parse_mode=None,
                           entities=None,
                           disable_web_page_preview=None,
                           disable_notification=None,
                           reply_to_message_id=None,
                           allow_sending_without_reply=None,
                           reply_markup=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(
            self._url + 'sendMessage',
            data=data,
            timeout=self.TIMEOUT
        )

    async def forward_message(self, chat_id, from_chat_id, message_id, disable_notification=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(
            self._url + 'forwardMessage',
            data=data,
            timeout=self.TIMEOUT
        )

    async def copy_message(self,
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

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(
            self._url + 'copyMessage',
            data=data,
            timeout=self.TIMEOUT
        )

    async def send_photo(self,
                         chat_id,
                         photo,
                         caption=None,
                         parse_mode=None,
                         disable_notification=None,
                         reply_to_message_id=None,
                         allow_sending_without_reply=None,
                         reply_markup=None):

        raise NotImplemented
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
        return await self._request(self._url + 'sendPhoto', data=kwargs, files=files_kwargs, timeout=self.TIMEOUT)

    async def send_audio(self,
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
        raise NotImplemented
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
        return await self._request(self._url + 'sendAudio', data=kwargs, files=files_kwargs, timeout=self.TIMEOUT)

    async def send_document(self,
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
        raise NotImplemented
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
        return await self._request(self._url + 'sendDocument', data=kwargs, files=files_kwargs, timeout=self.TIMEOUT)

    async def send_video(self,
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
        raise NotImplemented
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
        return await self._request(self._url + 'sendVideo', data=kwargs, files=files_kwargs, timeout=self.TIMEOUT)

    async def send_animation(self,
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
        raise NotImplemented
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
        return await self._request(self._url + 'sendAnimation', data=kwargs, files=files_kwargs, timeout=self.TIMEOUT)

    async def send_voice(self,
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
        raise NotImplemented
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
        return await self._request(self._url + 'sendVoice', data=kwargs, files=files_kwargs, timeout=self.TIMEOUT)

    async def send_video_note(self,
                              chat_id,
                              video_note,
                              duration=None,
                              length=None,
                              thumb=None,
                              disable_notification=None,
                              reply_to_message_id=None,
                              allow_sending_without_reply=None,
                              reply_markup=None):
        raise NotImplemented
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
        return await self._request(self._url + 'sendVideoNote', data=kwargs, files=files_kwargs, timeout=self.TIMEOUT)

    async def send_media_group(self,
                               chat_id,
                               media,
                               disable_notification=None,
                               reply_to_message_id=None,
                               allow_sending_without_reply=None):
        raise NotImplemented
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
        return await self._request(self._url + 'sendMediaGroup', data=kwargs, files=files_kwargs, timeout=self.TIMEOUT)

    async def send_location(self,
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

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(
            self._url + 'sendLocation',
            data=data,
            timeout=self.TIMEOUT
        )

    async def edit_message_live_location(self,
                                         latitude,
                                         longitude,
                                         chat_id=None,
                                         message_id=None,
                                         inline_message_id=None,
                                         horizontal_accuracy=None,
                                         heading=None,
                                         proximity_alert_radius=None,
                                         reply_markup=None):

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(
            self._url + 'editMessageLiveLocation',
            data=data,
            timeout=self.TIMEOUT
        )

    async def stop_message_live_location(self, chat_id=None, message_id=None, inline_message_id=None,
                                         reply_markup=None):

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'stopMessageLiveLocation', data=data, timeout=self.TIMEOUT)

    async def send_venue(self,
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

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'sendVenue', data=data, timeout=self.TIMEOUT)

    async def send_contact(self,
                           chat_id,
                           phone_number,
                           first_name,
                           last_name=None,
                           vcard=None,
                           disable_notification=None,
                           reply_to_message_id=None,
                           allow_sending_without_reply=None,
                           reply_markup=None):

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'sendContact', data=data, timeout=self.TIMEOUT)

    async def send_poll(self,
                        chat_id,
                        question,
                        options,
                        is_anonymous=None,
                        type_=None,
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

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'sendPoll', data=data, timeout=self.TIMEOUT)

    async def send_dice(self,
                        chat_id,
                        emoji=None,
                        disable_notification=None,
                        reply_to_message_id=None,
                        allow_sending_without_reply=None,
                        reply_markup=None):

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'sendDice', data=data, timeout=self.TIMEOUT)

    async def send_chat_action(self, chat_id, action):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(
            self._url + 'sendChatAction',
            data=data,
            timeout=self.TIMEOUT
        )

    async def get_user_profile_photos(self, user_id, offset=None, limit=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(
            self._url + 'getUserProfilePhotos',
            data=data,
            timeout=self.TIMEOUT
        )

    async def get_file(self, file_id):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'getFile', data=data, timeout=self.TIMEOUT)

    async def ban_chat_member(self, chat_id, user_id, until_date=None, revoke_messages=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'banChatMember', data=data, timeout=self.TIMEOUT)

    async def unban_chat_member(self, chat_id, user_id, only_if_banned=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'unbanChatMember', data=data, timeout=self.TIMEOUT)

    async def restrict_chat_member(self, chat_id, user_id, permissions, until_date=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'restrictChatMember', data=data, timeout=self.TIMEOUT)

    async def promote_chat_member(self,
                                  chat_id,
                                  user_id,
                                  is_anonymous=None,
                                  can_manage_chat=None,
                                  can_change_info=None,
                                  can_post_messages=None,
                                  can_edit_messages=None,
                                  can_delete_messages=None,
                                  can_manage_voice_chats=None,
                                  can_invite_users=None,
                                  can_restrict_members=None,
                                  can_pin_messages=None,
                                  can_promote_members=None):

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'promoteChatMember', data=data, timeout=self.TIMEOUT)

    async def set_chat_administrator_custom_title(self, chat_id, user_id, custom_title):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'setChatAdministratorCustomTitle', data=data, timeout=self.TIMEOUT)

    async def set_chat_permissions(self, chat_id, permissions):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(
            self._url + 'setChatPermissions',
            data=data,
            timeout=self.TIMEOUT
        )

    async def export_chat_invite_link(self, chat_id):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'exportChatInviteLink', data=data, timeout=self.TIMEOUT)

    async def create_chat_invite_link(self,
                                      chat_id,
                                      name=None,
                                      expire_date=None,
                                      member_limit=None,
                                      creates_join_request=None):

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'createChatInviteLink', data=data, timeout=self.TIMEOUT)

    async def edit_chat_invite_link(self,
                                    chat_id,
                                    invite_link,
                                    name=None,
                                    expire_date=None,
                                    member_limit=None,
                                    creates_join_request=None):

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'editChatInviteLink', data=data, timeout=self.TIMEOUT)

    async def revoke_chat_invite_link(self, chat_id, invite_link):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(
            self._url + 'revokeChatInviteLink',
            data=data,
            timeout=self.TIMEOUT
        )

    async def approve_chat_join_request(self, chat_id, user_id):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(
            self._url + 'approveChatJoinRequest',
            data=data,
            timeout=self.TIMEOUT
        )

    async def decline_chat_join_request(self, chat_id, user_id):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'declineChatJoinRequest', data=data, timeout=self.TIMEOUT)

    async def set_chat_photo(self, chat_id, photo):
        raise NotImplemented
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
        return await self._request(self._url + 'setChatPhoto', data=kwargs, files=files_kwargs, timeout=self.TIMEOUT)

    async def delete_chat_photo(self, chat_id):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'deleteChatPhoto', data=data, timeout=self.TIMEOUT)

    async def set_chat_title(self, chat_id, title):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'setChatTitle', data=data, timeout=self.TIMEOUT)

    async def set_chat_description(self, chat_id, description=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'setChatDescription',
                                   data=data,
                                   timeout=self.TIMEOUT)

    async def pin_chat_message(self, chat_id, message_id, disable_notification=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'pinChatMessage', data=data, timeout=self.TIMEOUT)

    async def unpin_chat_message(self, chat_id, message_id=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'unpinChatMessage', data=data, timeout=self.TIMEOUT)

    async def unpin_all_chat_messages(self, chat_id):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'unpinAllChatMessages', data=data, timeout=self.TIMEOUT)

    async def leave_chat(self, chat_id):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'leaveChat', data=data, timeout=self.TIMEOUT)

    async def get_chat(self, chat_id):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'getChat', data=data, timeout=self.TIMEOUT)

    async def get_chat_administrators(self, chat_id):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(
            self._url + 'getChatAdministrators',
            data=data, timeout=self.TIMEOUT
        )

    async def get_chat_member_count(self, chat_id):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'getChatMemberCount', data=data, timeout=self.TIMEOUT)

    async def get_chat_member(self, chat_id, user_id):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'getChatMember', data=data,
                                   timeout=self.TIMEOUT)

    async def set_chat_sticker_set(self, chat_id, sticker_set_name):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'setChatStickerSet',
                                   data=data, timeout=self.TIMEOUT)

    async def delete_chat_sticker_set(self, chat_id):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'deleteChatStickerSet', data=data, timeout=self.TIMEOUT)

    async def answer_callback_query(self,
                                    callback_query_id,
                                    text=None,
                                    show_alert=None,
                                    url=None,
                                    cache_time=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'answerCallbackQuery', data=data, timeout=self.TIMEOUT)

    async def set_my_commands(self, commands, scope=None, language_code=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'setMyCommands', data=data, timeout=self.TIMEOUT)

    async def delete_my_commands(self, scope=None, language_code=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'deleteMyCommands', data=data, timeout=self.TIMEOUT)

    async def get_my_commands(self, scope=None, language_code=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'getMyCommands', data=data, timeout=self.TIMEOUT)

    async def edit_message_text(self,
                                text,
                                chat_id=None,
                                message_id=None,
                                inline_message_id=None,
                                parse_mode=None,
                                entities=None,
                                disable_web_page_preview=None,
                                reply_markup=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'editMessageText', data=data, timeout=self.TIMEOUT)

    async def edit_message_caption(self,
                                   chat_id=None,
                                   message_id=None,
                                   inline_message_id=None,
                                   caption=None,
                                   parse_mode=None,
                                   caption_entities=None,
                                   reply_markup=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'editMessageCaption', data=data, timeout=self.TIMEOUT)

    async def edit_message_media(self, media, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'editMessageMedia', data=data, timeout=self.TIMEOUT)

    async def edit_message_reply_markup(self, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'editMessageReplyMarkup', data=data, timeout=self.TIMEOUT)

    async def stop_poll(self, chat_id, message_id, reply_markup=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'stopPoll', data=data, timeout=self.TIMEOUT)

    async def delete_message(self, chat_id, message_id):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'deleteMessage', data=data,
                                   timeout=self.TIMEOUT)

    async def send_sticker(self,
                           chat_id,
                           sticker,
                           disable_notification=None,
                           reply_to_message_id=None,
                           allow_sending_without_reply=None,
                           reply_markup=None):
        raise NotImplemented
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
        return await self._request(self._url + 'sendSticker', data=kwargs, files=files_kwargs, timeout=self.TIMEOUT)

    async def get_sticker_set(self, name):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'getStickerSet', data=data, timeout=self.TIMEOUT)

    async def upload_sticker_file(self, user_id, png_sticker):
        raise NotImplemented
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
        return await self._request(
            self._url + 'uploadStickerFile',
            data=kwargs,
            files=files_kwargs,
            timeout=self.TIMEOUT
        )

    async def create_new_sticker_set(self,
                                     user_id,
                                     name,
                                     title,
                                     emojis,
                                     png_sticker=None,
                                     tgs_sticker=None,
                                     contains_masks=None,
                                     mask_position=None):
        raise NotImplemented
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
        return await self._request(self._url + 'createNewStickerSet', data=kwargs, files_kwargs=files_kwargs,
                                   timeout=self.TIMEOUT)

    async def add_sticker_to_set(self, user_id, name, emojis, png_sticker=None, tgs_sticker=None, mask_position=None):
        raise NotImplemented
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
        return await self._request(self._url + 'addStickerToSet', data=kwargs, files_kwargs=files_kwargs,
                                   timeout=self.TIMEOUT)

    async def set_sticker_position_in_set(self, sticker, position):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'setStickerPositionInSet', data=data,
                                   timeout=self.TIMEOUT)

    async def delete_sticker_from_set(self, sticker):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'deleteStickerFromSet', data=data, timeout=self.TIMEOUT)

    async def set_sticker_set_thumb(self, name, user_id, thumb):
        raise NotImplemented
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
        return await self._request(self._url + 'setStickerSetThumb', data=kwargs, files_kwargs=files_kwargs,
                                   timeout=self.TIMEOUT)

    async def answer_inline_query(self,
                                  inline_query_id,
                                  results,
                                  cache_time=None,
                                  is_personal=None,
                                  next_offset=None,
                                  switch_pm_text=None,
                                  switch_pm_parameter=None):

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'answerInlineQuery', data=data, timeout=self.TIMEOUT)

    async def send_invoice(self,
                           chat_id,
                           title,
                           description,
                           payload,
                           provider_token,
                           currency,
                           prices,
                           start_parameter=None,
                           max_tip_amount=None,
                           suggested_tip_amounts=None,
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

        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'sendInvoice', data=data, timeout=self.TIMEOUT)

    async def answer_shipping_query(self, shipping_query_id, ok, shipping_options=None, error_message=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'answerShippingQuery', data=data, timeout=self.TIMEOUT)

    async def answer_pre_checkout_query(self, pre_checkout_query_id, ok, error_message=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'answerPreCheckoutQuery', data=data, timeout=self.TIMEOUT)

    async def set_passport_data_errors(self, user_id, errors):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'setPassportDataErrors', data=data,
                                   timeout=self.TIMEOUT)

    async def send_game(self,
                        chat_id,
                        game_short_name,
                        disable_notification=None,
                        reply_to_message_id=None,
                        allow_sending_without_reply=None,
                        reply_markup=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'sendGame', data=data, timeout=self.TIMEOUT)

    async def set_game_score(self,
                             user_id,
                             score,
                             force=None,
                             disable_edit_message=None,
                             chat_id=None,
                             message_id=None,
                             inline_message_id=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'setGameScore', data=data, timeout=self.TIMEOUT)

    async def get_game_high_scores(self, user_id, chat_id=None, message_id=None, inline_message_id=None):
        data = {k: v for k, v in locals().items() if v is not None and k != 'self'}
        return await self._request(self._url + 'getGameHighScores', data=data, timeout=self.TIMEOUT)
