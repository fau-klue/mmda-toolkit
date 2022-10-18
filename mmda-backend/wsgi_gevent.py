from gevent.pywsgi import WSGIServer
from backend import create_app

app = create_app()

http_server = WSGIServer((app.config['APP_HOST'], app.config['APP_PORT']),
                         app,
                         app.config['APP_TLS_KEYFILE'],
                         app.config['APP_TLS_CERTFILE'])

http_server.serve_forever()
