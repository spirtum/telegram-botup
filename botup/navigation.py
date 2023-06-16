from __future__ import annotations

from typing import List

from botup.exceptions import WidgetNotInRegistryError
from botup.widget import WidgetRegistry, Widget, Context


class Navigation:

    def __init__(self, context: Context, path: str):
        path = path or context.root_widget.key
        widget_registry = WidgetRegistry()
        self._context = context

        try:
            self._stack: List[Widget] = [widget_registry.get(key) for key in path.split('/')]
        except WidgetNotInRegistryError:
            self._stack: List[Widget] = [context.root_widget]

    @property
    def current_widget(self) -> Widget:
        return self._stack[-1]

    @classmethod
    async def of(cls, context: Context) -> Navigation:
        path = await context.get_path()
        return Navigation(context, path)

    async def push(self, key: str, **kwargs):
        if not self.current_widget.is_children_by_key(key):
            raise Exception(f'Key "{key}" is not children for current widget "{self.current_widget.key}"')  # TODO: specify exception

        if not self._context.chat_id:
            raise Exception("Can't resolve chat_id from current update")  # TODO: specify exception

        self._stack.append(WidgetRegistry().get(key))
        await self._context.state_manager.set_path(self._context.chat_id, self.path())
        await self.current_widget.entry(self._context, **kwargs)

    async def pop(self, **kwargs):
        if not self._context.chat_id:
            raise Exception("Can't resolve chat_id from current update")  # TODO: specify exception

        self._stack.pop()
        await self._context.state_manager.set_path(self._context.chat_id, self.path())
        await self.current_widget.entry(self._context, **kwargs)

    def path(self) -> str:
        return '/'.join((w.key for w in self._stack))
