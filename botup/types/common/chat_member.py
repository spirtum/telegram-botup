from .user import User


class ChatMember:

    def __init__(self, **kwargs):
        self.user = User(**kwargs.get('user'))
        self.status = kwargs.get('status')
        self.until_date = kwargs.get('until_date')
        self.can_be_edited = kwargs.get('can_be_edited')
        self.can_change_info = kwargs.get('can_change_info')
        self.can_post_messages = kwargs.get('can_post_messages')
        self.can_edit_messages = kwargs.get('can_edit_messages')
        self.can_delete_messages = kwargs.get('can_delete_messages')
        self.can_invite_users = kwargs.get('can_invite_users')
        self.can_restrict_members = kwargs.get('can_restrict_members')
        self.can_pin_messages = kwargs.get('can_pin_messages')
        self.can_promote_members = kwargs.get('can_promote_members')
        self.is_member = kwargs.get('is_member')
        self.can_send_messages = kwargs.get('can_send_messages')
        self.can_send_media_messages = kwargs.get('can_send_media_messages')
        self.can_send_other_messages = kwargs.get('can_send_other_messages')
        self.can_add_web_page_previews = kwargs.get('can_add_web_page_previews')
