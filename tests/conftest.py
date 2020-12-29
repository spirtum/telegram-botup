import pytest
from botup import Dispatcher


@pytest.fixture
def dispatcher():
    return Dispatcher()
