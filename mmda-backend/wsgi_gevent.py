from gevent.pywsgi import WSGIServer
from backend import create_app

app = create_app()

http_server = WSGIServer(listener=(app.config['APP_HOST'], app.config['APP_PORT']),
                         application=app,
                         keyfile=app.config['APP_TLS_KEYFILE'],
                         certfile=app.config['APP_TLS_CERTFILE'])

http_server.serve_forever()
