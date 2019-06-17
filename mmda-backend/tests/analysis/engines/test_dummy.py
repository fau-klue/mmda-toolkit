import pytest

from backend.analysis.engines import *

@pytest.mark.engine
def test_dummy_engine_inheritance():

    assert issubclass(DummyEngine, Engine)
