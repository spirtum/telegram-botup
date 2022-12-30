from .core.types import Update
from .state_manager.base import StateManager, DictStateManager
from .navigation import Navigation
from .widget import Widget, BuildContext


class Bot:

    def __init__(
            self,
            root_widget: Widget,
            state_manager: StateManager = DictStateManager()
    ):
        self._root_widget = root_widget
        self._state_manager = state_manager

    async def handle(self, update: dict):
        update = Update.from_dict(update)
        context = BuildContext(update, self._root_widget, self._state_manager)
        navigation = await Navigation.of(context)
        await navigation.current_widget.handle(context)
