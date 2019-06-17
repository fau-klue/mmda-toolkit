import pytest

from backend.analysis.engines import *

@pytest.mark.engine
def test_random_engine_inheritance():
    assert issubclass(RandomEngine, Engine)
