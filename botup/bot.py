from typing import Type

from .core.types import Update
from .helpers import StateManager, DictStateManager
from .navigation import Navigation
from .widget import Widget, BuildContext


class Bot:

    def __init__(self, root_widget: Widget, state_manager_class: Type[StateManager] = DictStateManager):
        self._root_widget = root_widget
        self._state_manager_class = state_manager_class

    async def handle(self, update: dict):
        update = Update.from_dict(update)
        context = BuildContext(update, self._root_widget, self._state_manager_class())
        navigation = await Navigation.of(context)
        await navigation.current_widget.handle(context)
