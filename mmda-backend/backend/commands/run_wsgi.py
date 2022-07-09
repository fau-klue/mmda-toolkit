"""
Run Flask in production environment
"""


from backend import create_app
from flask_script import Command
from gevent.pywsgi import WSGIServer


class WSGICommand(Command):
    """
    Run the production server. Flask Command Interface.
    """

    def run(self):
        run_wsgi()


def run_wsgi():
    """
    Starts the API with a WSGI Server for production use.
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

    print('Started WSGI Server on {host}:{port}.'.format(host=APP_HOST, port=APP_PORT))
    server.serve_forever()
