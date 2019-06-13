import pytest

from backend.analysis.engines import *

def test_dummy_engine_inheritance():

    assert issubclass(DummyEngine, Engine)
