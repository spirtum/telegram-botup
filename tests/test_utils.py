from botup.utils import get_chat_id

from tests import utils


def test_get_chat_id_with_inline_query():
    update = utils.inline_query_update_by_query('example')
    assert get_chat_id(update) == update.inline_query.from_.id
