# __init__.py is a special Python file that allows a directory to become
# a Python package so it can be accessed using the 'import' statement.

__all__ = ['DummyEngine', 'CWBEngine', 'Engine']

from .engine import Engine
from .dummy import DummyEngine
from .cwb import CWBEngine
