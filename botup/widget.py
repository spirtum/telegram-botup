from __future__ import annotations

from typing import Dict, Optional, List

from .core.dispatcher import Dispatcher
from .core.types import Update, Context
from .state_manager.base import Singleton, StateManager


class WidgetRegistry(metaclass=Singleton):

    def __init__(self):
        self._data: Dict[str, Widget] = {}

    def add(self, widget: Widget):
        self._data[widget.key] = widget

    def get(self, key: str) -> Widget:
        return self._data[key]


class Widget:

    def __init__(self, key: str):
        self.key = key
        self._dispatcher = Dispatcher()
        self.build(self._dispatcher)
        self.children = self.build_children()
        WidgetRegistry().add(self)

    @staticmethod
    async def entry(context: BuildContext):
        raise NotImplementedError()

    async def build(self, dispatcher: Dispatcher):
        raise NotImplementedError()

    @staticmethod
    async def build_children() -> List[Widget]:
        return []

    async def handle(self, context: BuildContext):
        await self._dispatcher.handle_context(context)


class BuildContext(Context):

    def __init__(self, update: Update, root_widget: Widget, state_manager: StateManager):
        super().__init__(update)
        self.state_manager = state_manager
        self.root_widget = root_widget

    async def get_path(self) -> str:
        return await self.state_manager.get(self.chat_id or self.get_chat_id()) or ''

    def get_chat_id(self) -> Optional[int]:
        if self.is_message:
            return self.update.message.chat.id

        if self.is_callback_query:
            return self.update.callback_query.from_.id

        if self.is_inline_query:
            return self.update.inline_query.from_.id

        return None
