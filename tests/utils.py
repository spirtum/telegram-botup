from botup.types import Update

USER_FIRST_NAME = 'FirstName'
USER_LAST_NAME = 'LastName'
USER_USERNAME = 'username'
USER_ID = 123456789
BOT_NAME = 'BotName'
BOT_USERNAME = 'botusername'
BOT_ID = 987654321
GROUP_TITLE = 'GroupTitle'
GROUP_ID = -456123789
CHANNEL_TITLE = 'ChannelTitle'
CHANNEL_ID = -654321987


def message_update_by_text(text):
    return Update(**{'message': {'chat': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'last_name': USER_LAST_NAME,
                                          'type': 'private',
                                          'username': USER_USERNAME},
                                 'date': 1579384330,
                                 'from': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'is_bot': False,
                                          'language_code': 'en',
                                          'last_name': USER_LAST_NAME,
                                          'username': USER_USERNAME},
                                 'message_id': 10590,
                                 'text': text},
                     'update_id': 751167721})


def command_update_by_text(text):
    return Update(**{'message': {'chat': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'last_name': USER_LAST_NAME,
                                          'type': 'private',
                                          'username': USER_USERNAME},
                                 'date': 1579426411,
                                 'entities': [{'length': 6, 'offset': 0, 'type': 'bot_command'}],
                                 'from': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'is_bot': False,
                                          'language_code': 'en',
                                          'last_name': USER_LAST_NAME,
                                          'username': USER_USERNAME},
                                 'message_id': 10594,
                                 'text': text},
                     'update_id': 751167722})


def callback_update_by_data(data):
    return Update(**{'callback_query': {'chat_instance': '123',
                                        'data': data,
                                        'from': {'first_name': USER_FIRST_NAME,
                                                 'id': USER_ID,
                                                 'is_bot': False,
                                                 'language_code': 'en',
                                                 'last_name': USER_LAST_NAME,
                                                 'username': USER_USERNAME},
                                        'id': '123',
                                        'message': {'chat': {'first_name': USER_FIRST_NAME,
                                                             'id': USER_ID,
                                                             'last_name': USER_LAST_NAME,
                                                             'type': 'private',
                                                             'username': USER_USERNAME},
                                                    'date': 123,
                                                    'from_': {'first_name': BOT_NAME,
                                                              'id': BOT_ID,
                                                              'is_bot': True,
                                                              'username': BOT_USERNAME},
                                                    'message_id': 123,
                                                    'text': 'test'}},
                     'update_id': 123})


def inline_query_update_by_query(query):
    return Update(**{'inline_query': {'from': {'first_name': USER_FIRST_NAME,
                                               'id': USER_ID,
                                               'is_bot': False,
                                               'language_code': 'en',
                                               'last_name': USER_LAST_NAME,
                                               'username': USER_USERNAME},
                                      'id': '123',
                                      'offset': '',
                                      'query': query},
                     'update_id': 123})


def chosen_inline_result_update():
    return Update(**{'chosen_inline_result': {'from': {'first_name': USER_FIRST_NAME,
                                                       'id': USER_ID,
                                                       'is_bot': False,
                                                       'language_code': 'en',
                                                       'last_name': USER_LAST_NAME,
                                                       'username': USER_USERNAME},
                                              'query': 'share',
                                              'result_id': '1'},
                     'update_id': 123})


def edited_message_update_by_text(text):
    return Update(**{'edited_message': {'chat': {'first_name': USER_FIRST_NAME,
                                                 'id': USER_ID,
                                                 'last_name': USER_LAST_NAME,
                                                 'type': 'private',
                                                 'username': USER_USERNAME},
                                        'date': 123,
                                        'edit_date': 123,
                                        'from': {'first_name': USER_FIRST_NAME,
                                                 'id': USER_ID,
                                                 'is_bot': False,
                                                 'language_code': 'en',
                                                 'last_name': USER_LAST_NAME,
                                                 'username': USER_USERNAME},
                                        'message_id': 123,
                                        'text': text},
                     'update_id': 123})


def channel_post_update():
    return Update(**{'channel_post': {'chat': {'id': CHANNEL_ID,
                                               'title': CHANNEL_TITLE,
                                               'type': 'channel'},
                                      'date': 123,
                                      'message_id': 2,
                                      'text': 'Channel post'},
                     'update_id': 123})


def edited_channel_post_update():
    return Update(**{'edited_channel_post': {'chat': {'id': CHANNEL_ID,
                                                      'title': CHANNEL_TITLE,
                                                      'type': 'channel'},
                                             'date': 123,
                                             'edit_date': 124,
                                             'message_id': 2,
                                             'text': 'Channel post 1234'},
                     'update_id': 123})


def dice_update():
    return Update(**{'message': {'chat': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'last_name': USER_LAST_NAME,
                                          'type': 'private',
                                          'username': USER_USERNAME},
                                 'date': 123,
                                 'dice': {'value': 6},
                                 'from': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'is_bot': False,
                                          'language_code': 'en',
                                          'last_name': USER_LAST_NAME,
                                          'username': USER_USERNAME},
                                 'message_id': 2},
                     'update_id': 123})


def document_update():
    return Update(**{'message': {'chat': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'last_name': USER_LAST_NAME,
                                          'type': 'private',
                                          'username': USER_USERNAME},
                                 'date': 123,
                                 'document': {'file_id': '123',
                                              'file_name': 'Title.txt',
                                              'file_size': 105,
                                              'file_unique_id': 'asfa',
                                              'mime_type': 'text/plain'},
                                 'from': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'is_bot': False,
                                          'language_code': 'en',
                                          'last_name': USER_LAST_NAME,
                                          'username': USER_USERNAME},
                                 'message_id': 123},
                     'update_id': 123})


def animation_update():
    return Update(**{'message': {'animation': {'duration': 3,
                                               'file_id': 'qwe',
                                               'file_name': 'giphy.mp4',
                                               'file_size': 253953,
                                               'file_unique_id': 'asd',
                                               'height': 270,
                                               'mime_type': 'video/mp4',
                                               'thumb': {
                                                   'file_id': 'qwe',
                                                   'file_size': 16022,
                                                   'file_unique_id': 'asd',
                                                   'height': 180,
                                                   'width': 320},
                                               'width': 480},
                                 'chat': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'last_name': USER_LAST_NAME,
                                          'type': 'private',
                                          'username': USER_USERNAME},
                                 'date': 123,
                                 'document': {'file_id': 'qwe',
                                              'file_name': 'giphy.mp4',
                                              'file_size': 253953,
                                              'file_unique_id': 'asd',
                                              'mime_type': 'video/mp4',
                                              'thumb': {
                                                  'file_id': 'qwe',
                                                  'file_size': 16022,
                                                  'file_unique_id': 'asd',
                                                  'height': 180,
                                                  'width': 320}},
                                 'from': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'is_bot': False,
                                          'language_code': 'en',
                                          'last_name': USER_LAST_NAME,
                                          'username': USER_USERNAME},
                                 'message_id': 123},
                     'update_id': 123})


def audio_update():
    return Update(**{'message': {'audio': {'duration': 187,
                                           'file_id': 'qwe-_ustVZpRYE',
                                           'file_size': 3005143,
                                           'file_unique_id': 'asd',
                                           'mime_type': 'audio/mpeg',
                                           'performer': 'Performer',
                                           'title': 'Title'},
                                 'chat': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'last_name': USER_LAST_NAME,
                                          'type': 'private',
                                          'username': USER_USERNAME},
                                 'date': 123,
                                 'from_': {'first_name': USER_FIRST_NAME,
                                           'id': USER_ID,
                                           'is_bot': False,
                                           'language_code': 'en',
                                           'last_name': USER_LAST_NAME,
                                           'username': USER_USERNAME},
                                 'message_id': 123},
                     'update_id': 123})


def contact_update():
    return Update(**{'message': {'chat': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'last_name': USER_LAST_NAME,
                                          'type': 'private',
                                          'username': USER_USERNAME},
                                 'contact': {'first_name': USER_FIRST_NAME,
                                             'phone_number': '+123456789',
                                             'user_id': USER_ID,
                                             'vcard': 'BEGIN:VCARD \n'
                                                      'VERSION:3.0 \n'
                                                      'PRODID:-//Apple Inc.//iPhone OS '
                                                      '13.1.2//EN \n'
                                                      'N:;ContactName;;; \n'
                                                      'FN:ContactName \n'
                                                      'TEL;type=CELL;type=VOICE;type=pref:+123456789 \n'
                                                      'END:VCARD \n'},
                                 'date': 123,
                                 'from_': {'first_name': USER_FIRST_NAME,
                                           'id': USER_ID,
                                           'is_bot': False,
                                           'language_code': 'en',
                                           'last_name': USER_LAST_NAME,
                                           'username': USER_USERNAME},
                                 'message_id': 123},
                     'update_id': 123})


def new_chat_members_update():
    return Update(**{'message': {'chat': {'id': GROUP_ID,
                                          'title': GROUP_TITLE,
                                          'type': 'group'},
                                 'date': 123,
                                 'from': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'is_bot': False,
                                          'language_code': 'en',
                                          'last_name': USER_LAST_NAME,
                                          'username': USER_USERNAME},
                                 'message_id': 123,
                                 'new_chat_members': [{'first_name': BOT_NAME,
                                                       'id': BOT_ID,
                                                       'is_bot': True,
                                                       'username': BOT_USERNAME}]},
                     'update_id': 123})


def new_chat_title_update():
    return Update(**{'message': {'chat': {'id': GROUP_ID,
                                          'title': GROUP_TITLE,
                                          'type': 'group'},
                                 'date': 123,
                                 'from': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'is_bot': False,
                                          'language_code': 'en',
                                          'last_name': USER_LAST_NAME,
                                          'username': USER_USERNAME},
                                 'message_id': 123,
                                 'new_chat_title': GROUP_TITLE},
                     'update_id': 123})


def new_chat_photo_update():
    return Update(**{'message': {'chat': {'id': GROUP_ID,
                                          'title': GROUP_TITLE,
                                          'type': 'group'},
                                 'date': 123,
                                 'from': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'is_bot': False,
                                          'language_code': 'en',
                                          'last_name': USER_LAST_NAME,
                                          'username': USER_USERNAME},
                                 'message_id': 123,
                                 'new_chat_photo': [
                                     {'file_id': 'qwe',
                                      'file_size': 5790,
                                      'file_unique_id': 'asd',
                                      'height': 160,
                                      'width': 160},
                                     {'file_id': 'qwe',
                                      'file_size': 17376,
                                      'file_unique_id': 'asd',
                                      'height': 320,
                                      'width': 320},
                                     {'file_id': 'qwe',
                                      'file_size': 58606,
                                      'file_unique_id': 'asd',
                                      'height': 640,
                                      'width': 640}]},
                     'update_id': 123})


def left_chat_member_update():
    return Update(**{'message': {'chat': {'id': GROUP_ID,
                                          'title': GROUP_TITLE,
                                          'type': 'group'},
                                 'date': 123,
                                 'from': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'is_bot': False,
                                          'language_code': 'en',
                                          'last_name': USER_LAST_NAME,
                                          'username': USER_USERNAME},
                                 'left_chat_member': {'first_name': BOT_NAME,
                                                      'id': BOT_ID,
                                                      'is_bot': True,
                                                      'username': BOT_USERNAME},
                                 'message_id': 123},
                     'update_id': 123})


def location_update():
    return Update(**{'message': {'chat': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'last_name': USER_LAST_NAME,
                                          'type': 'private',
                                          'username': USER_USERNAME},
                                 'date': 123,
                                 'from': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'is_bot': False,
                                          'language_code': 'en',
                                          'last_name': USER_LAST_NAME,
                                          'username': USER_USERNAME},
                                 'location': {'latitude': 11.111111, 'longitude': 11.111111},
                                 'message_id': 123},
                     'update_id': 123})


def poll_update():
    return Update(**{'poll': {'id': '123',
                              'is_closed': False,
                              'options': [{'text': 'option1', 'voter_count': 1},
                                          {'text': 'option2', 'voter_count': 0},
                                          {'text': 'option3', 'voter_count': 0}],
                              'question': 'question?'},
                     'update_id': 123})


def poll_answer_update():
    return Update(**{'poll_answer': {'option_ids': [0],
                                     'poll_id': '123',
                                     'user': {'first_name': USER_FIRST_NAME,
                                              'id': USER_ID,
                                              'is_bot': False,
                                              'language_code': 'en',
                                              'last_name': USER_LAST_NAME,
                                              'username': USER_USERNAME}},
                     'update_id': 123})


def photo_update():
    return Update(**{'message': {'chat': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'last_name': USER_LAST_NAME,
                                          'type': 'private',
                                          'username': USER_USERNAME},
                                 'date': 123,
                                 'from': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'is_bot': False,
                                          'language_code': 'en',
                                          'last_name': USER_LAST_NAME,
                                          'username': USER_USERNAME},
                                 'message_id': 123,
                                 'photo': [{'file_id': 'qwe',
                                            'file_size': 12292,
                                            'file_unique_id': 'asd',
                                            'height': 320,
                                            'width': 320},
                                           {'file_id': 'qwe',
                                            'file_size': 46695,
                                            'file_unique_id': 'asd',
                                            'height': 640,
                                            'width': 640}]},
                     'update_id': 123})


def sticker_update():
    return Update(**{'message': {'chat': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'last_name': USER_LAST_NAME,
                                          'type': 'private',
                                          'username': USER_USERNAME},
                                 'date': 123,
                                 'from': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'is_bot': False,
                                          'language_code': 'en',
                                          'last_name': USER_LAST_NAME,
                                          'username': USER_USERNAME},
                                 'message_id': 123,
                                 'sticker': {'emoji': '😊',
                                             'file_id': 'qwe',
                                             'file_size': 56464,
                                             'file_unique_id': 'asd',
                                             'height': 512,
                                             'is_animated': False,
                                             'set_name': 'pussycat',
                                             'thumb': {
                                                 'file_id': 'qwe-ifbCEKgAEAQAHbQADeAoAAhYE',
                                                 'file_size': 5648,
                                                 'file_unique_id': 'asd',
                                                 'height': 128,
                                                 'width': 128},
                                             'width': 512}},
                     'update_id': 123})


def video_update():
    return Update(**{'message': {'chat': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'last_name': USER_LAST_NAME,
                                          'type': 'private',
                                          'username': USER_USERNAME},
                                 'date': 123,
                                 'from': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'is_bot': False,
                                          'language_code': 'en',
                                          'last_name': USER_LAST_NAME,
                                          'username': USER_USERNAME},
                                 'message_id': 123,
                                 'video': {'duration': 5,
                                           'file_id': 'qwe',
                                           'file_size': 537084,
                                           'file_unique_id': 'asd',
                                           'height': 560,
                                           'mime_type': 'video/mp4',
                                           'thumb': {'file_id': 'qwe',
                                                     'file_size': 14353,
                                                     'file_unique_id': 'asd',
                                                     'height': 320,
                                                     'width': 182},
                                           'width': 320}},
                     'update_id': 123})


def video_note_update():
    return Update(**{'message': {'chat': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'last_name': USER_LAST_NAME,
                                          'type': 'private',
                                          'username': USER_USERNAME},
                                 'date': 123,
                                 'from': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'is_bot': False,
                                          'language_code': 'en',
                                          'last_name': USER_LAST_NAME,
                                          'username': USER_USERNAME},
                                 'message_id': 123,
                                 'video_note': {'duration': 3,
                                                'file_id': 'qwe-vHFBYE',
                                                'file_size': 156977,
                                                'file_unique_id': 'asd',
                                                'length': 240,
                                                'thumb': {
                                                    'file_id': 'qwe',
                                                    'file_size': 8225,
                                                    'file_unique_id': 'asd',
                                                    'height': 240,
                                                    'width': 240}}},
                     'update_id': 123})


def voice_update():
    return Update(**{'message': {'chat': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'last_name': USER_LAST_NAME,
                                          'type': 'private',
                                          'username': USER_USERNAME},
                                 'date': 123,
                                 'from': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'is_bot': False,
                                          'language_code': 'en',
                                          'last_name': USER_LAST_NAME,
                                          'username': USER_USERNAME},
                                 'message_id': 123,
                                 'voice': {'duration': 2,
                                           'file_id': 'qwe',
                                           'file_size': 10927,
                                           'file_unique_id': 'asas',
                                           'mime_type': 'audio/ogg'}},
                     'update_id': 123})


def venue_update():
    return Update(**{'message': {'chat': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'last_name': USER_LAST_NAME,
                                          'type': 'private',
                                          'username': USER_USERNAME},
                                 'date': 123,
                                 'from': {'first_name': USER_FIRST_NAME,
                                          'id': USER_ID,
                                          'is_bot': False,
                                          'language_code': 'en',
                                          'last_name': USER_LAST_NAME,
                                          'username': USER_USERNAME},
                                 'location': {'latitude': 11.111111, 'longitude': 11.111111},
                                 'message_id': 123,
                                 'venue': {'address': 'street, number',
                                           'foursquare_id': 'abcdef123456789',
                                           'foursquare_type': 'food/coffeeshop',
                                           'location': {'latitude': 11.111111,
                                                        'longitude': 11.111111},
                                           'title': 'VenueTitle'}},
                     'update_id': 123})
