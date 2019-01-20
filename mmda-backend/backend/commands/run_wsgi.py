"""
Run Flask in production environment
"""


from backend import create_app
from flask_script import Command
from os import getenv
from gevent.pywsgi import WSGIServer


class WSGICommand(Command):
    """
    Run the production server
    """

    def run(self):
        print('Started WSGI Server.')
        run_wsgi()


def run_wsgi():
    """
    Where the magic happens
    """

    app = create_app()

    APP_HOST = app.config['MMDA_APP_HOST']
    APP_PORT = app.config['MMDA_APP_PORT']

    server = WSGIServer(listener=(APP_HOST, APP_PORT),
                        application=app)

    if app.config['APP_TLS_ENABLE']:
        server = WSGIServer(listener=(APP_HOST, APP_PORT),
                            application=app,
                            keyfile=app.config['APP_TLS_KEYFILE'],
                            certfile=app.config['APP_TLS_CERTFILE'])

    server.serve_forever()
