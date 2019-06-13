import pytest

from backend.analysis.engines import *

def test_cwb_engine_inheritance():
    assert issubclass(CWBEngine, Engine)
