from botup.api import Api
from botup.types import Update
from botup.navigation import Navigation
from botup.state_manager.base import StateManager, DictStateManager
from botup.widget import Widget, Context


class Bot:

    def __init__(
            self,
            token: str,
            root_widget: Widget,
            state_manager: StateManager = DictStateManager(),
            api_timeout: int = 5
    ):
        self._api = Api(token, api_timeout)
        self._root_widget = root_widget
        self._state_manager = state_manager

    async def close_session(self):
        await self._api.close_session()

    async def handle(self, update: dict):
        update = Update.from_dict(update)
        context = Context(update, self._api, self._root_widget, self._state_manager)
        navigation = await Navigation.of(context)
        await navigation.current_widget.handle(context)
