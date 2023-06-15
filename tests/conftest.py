import pytest
from botup.dispatcher import Dispatcher


@pytest.fixture
def dispatcher():
    return Dispatcher()
