from gevent.pywsgi import WSGIServer
import logging
from common import app
from config import DEFAULT_HOST

logger = logging.getLogger(__name__)


def start():
    logger.info("Starting server.")
    http_server = WSGIServer(DEFAULT_HOST, app)
    logger.info("Listening on {}.".format(DEFAULT_HOST))
    http_server.serve_forever()
