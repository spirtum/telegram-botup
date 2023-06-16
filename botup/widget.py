from __future__ import annotations

from typing import Dict, Optional, List

from botup.api import Api
from botup.dispatcher import Dispatcher
from botup.types import Update, BaseContext
from botup.state_manager.base import Singleton, StateManager
from botup.exceptions import WidgetNotInRegistryError


class WidgetRegistry(metaclass=Singleton):

    def __init__(self):
        self._registry: Dict[str, Widget] = {}

    def add(self, widget: Widget):
        if widget.key in self._registry:
            raise Exception('Widget key already in WidgetRegistry')  # TODO: specify exception
        self._registry[widget.key] = widget

    def get(self, key: str) -> Widget:
        if key not in self._registry:
            raise WidgetNotInRegistryError(f'Widget with key "{key}" not found')
        return self._registry[key]


class Widget:

    def __init__(
            self,
            key: Optional[str] = None,
            children: Optional[List[Widget]] = None
    ):

        self.key = key or self.__class__.__name__
        self._dispatcher = Dispatcher()
        self.children = children or []
        self._children_keys = [w.key for w in self.children]
        self.build(self._dispatcher)
        WidgetRegistry().add(self)

    def build(self, dispatcher: Dispatcher):
        pass

    async def entry(self, ctx: Context, **kwargs):
        pass

    async def handle(self, ctx: Context):
        await self._dispatcher.handle_context(ctx)

    def is_children_by_key(self, key: str) -> bool:
        return key in self._children_keys


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
            return self.update.callback_query.message.chat.id

        if self.is_inline_query:
            return self.update.inline_query.from_.id

        return None

    async def quick_callback_answer(self):
        if not self.is_callback_query:
            raise Exception('Current update is not callback query')  # TODO: specify exception
        await self.api.answer_callback_query(self.update.callback_query.id)
