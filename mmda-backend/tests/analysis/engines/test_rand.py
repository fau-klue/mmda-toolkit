import pytest

from backend.analysis.engines import *

def test_random_engine_inheritance():
    assert issubclass(RandomEngine, Engine)
