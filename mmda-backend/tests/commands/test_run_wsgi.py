import pytest
import unittest.mock as mock

from backend.commands.run_wsgi import WSGICommand


@mock.patch('backend.commands.run_wsgi.WSGIServer')
def test_run_wsgi(mock_gevent):

    server = WSGICommand()
    server.run()

    assert mock_gevent.call_count == 1
