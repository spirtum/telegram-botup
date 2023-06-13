import pytest
from botup.core.dispatcher import Dispatcher


@pytest.fixture
def dispatcher():
    return Dispatcher()
