from gevent.pywsgi import WSGIServer
import logging
from .app import app
from .static.constants import LISTENER

logger = logging.getLogger(__name__)


def start():
    logger.info("Starting server.")
    http_server = WSGIServer(LISTENER, app)
    logger.info("Listening on {}.".format(LISTENER))
    http_server.serve_forever()
    logger.info("Bye-bye")
