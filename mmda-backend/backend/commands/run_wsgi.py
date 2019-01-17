"""
Run Flask in production environment
"""


from backend import create_app
from flask_script import Command
from os import getenv
from gevent.pywsgi import WSGIServer


# Get Host and Port from environment, to make Docker life esier
APP_HOST = str(getenv('MMDA_HOST', default='0.0.0.0'))
APP_PORT = int(getenv('MMDA_PORT', default='5000'))


class WSGICommand(Command):
    """
    Run the production server
    """

    def run(self):
        run_wsgi()


def run_wsgi():
    """
    Where the magic happens
    """

    # TODO: Add SSL Config
    # keyfile=app.config['APP_TLS_KEYFILE']
    # certfile=app.config['APP_TLS_CERTFILE']

    app = create_app()
    server = WSGIServer(listener=(APP_HOST, APP_PORT),
                        application=app)

    server.serve_forever()
