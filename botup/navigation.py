from __future__ import annotations

from typing import List

from botup.widget import WidgetRegistry, Widget, Context


class Navigation:

    def __init__(self, context: Context, path: str):
        path = path or context.root_widget.key
        _widget_registry = WidgetRegistry()
        self._context = context
        self._stack: List[Widget] = [_widget_registry.get(key) for key in path.split('/')]

    @property
    def current_widget(self) -> Widget:
        return self._stack[-1]

    @classmethod
    async def of(cls, context: Context) -> Navigation:
        path = await context.get_path()
        return Navigation(context, path)

    async def push(self, name: str, **kwargs):
        assert name in (w.key for w in self.current_widget.children)
        self._stack.append(WidgetRegistry().get(name))
        await self._context.state_manager.set_path(self._context.chat_id, self.path())
        await self.current_widget.entry(self._context, **kwargs)

    async def pop(self, **kwargs):
        self._stack.pop()
        await self._context.state_manager.set_path(self._context.chat_id, self.path())
        await self.current_widget.entry(self._context, **kwargs)

    def path(self) -> str:
        return '/'.join((w.key for w in self._stack))
