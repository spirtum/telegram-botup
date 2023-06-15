from __future__ import annotations

from typing import Dict, Optional, List

from botup.api import Api
from botup.dispatcher import Dispatcher
from botup.types import Update, BaseContext
from botup.state_manager.base import Singleton, StateManager


class WidgetRegistry(metaclass=Singleton):

    def __init__(self):
        self._data: Dict[str, Widget] = {}

    def add(self, widget: Widget):
        self._data[widget.key] = widget

    def get(self, key: str) -> Widget:
        return self._data[key]


class Widget:

    def __init__(self, key: str, children: Optional[List[Widget]] = None):
        self.key = key
        self._dispatcher = Dispatcher()
        self.children = children or []
        self.build(self._dispatcher)
        WidgetRegistry().add(self)

    async def entry(self, ctx: Context, **kwargs):
        pass

    def build(self, dispatcher: Dispatcher):
        pass

    async def handle(self, ctx: Context):
        await self._dispatcher.handle_context(ctx)


class Context(BaseContext):

    def __init__(
            self,
            update: Update,
            api: Api,
            root_widget: Widget,
            state_manager: StateManager
    ):
        super().__init__(update)
        self.api = api
        self.root_widget = root_widget
        self.state_manager = state_manager

    async def get_path(self) -> str:
        return await self.state_manager.get_path(self.chat_id or self.get_chat_id()) or ''

    def get_chat_id(self) -> Optional[int]:
        if self.is_message:
            return self.update.message.chat.id

        if self.is_callback_query:
            return self.update.callback_query.from_.id

        if self.is_inline_query:
            return self.update.inline_query.from_.id

        return None

    async def quick_callback_answer(self):
        assert self.is_callback_query
        await self.api.answer_callback_query(self.update.callback_query.id)
