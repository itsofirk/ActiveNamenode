import logging
import requests
from time import time
from .kerberos import get_token
from .app import app
from .static import constants
from flask import request

from .static.exceptions import ActiveNamenodeFailedToFoundException

ACTIVE = 'active'

logger = logging.getLogger(__name__)
namenodes_cache = {}


def get_active_namenode(environment):
    if environment in namenodes_cache:
        nn, ts = namenodes_cache[environment]
        if ts + constants.REFRESH_INTERVAL > time():
            logger.debug("Returns cached namenode")
            return nn
    logger.debug("Querying active namenode for {}".format(environment))
    nn_list, kerberized = constants.namenodes[environment]
    for nn in nn_list:
        try:
            logger.debug("Querying {}".format(nn))
            auth = None
            if kerberized:
                auth = get_token("anonymous@domain.dom", "b64_password")
            response = requests.get(constants.NAMENODE_URL.format(
                NAMENODE=nn,
                PORT=constants.WEBHDFS_DEFAULT_PORT,
                URI=constants.URI_QUERY
            ), auth=auth)
            if response.status_code != constants.HTTP_200_OK:
                logger.exception(response.text)
            if ACTIVE in response.text:
                logger.info("Active namenode for {} : {}".format(environment, nn))
                namenodes_cache.update({environment: (nn, time())})
                return nn
        except Exception as e:
            logger.exception(e)
    raise ActiveNamenodeFailedToFoundException('No Active Namenode found.')


@app.route('/index')
@app.route('/')
def index():
    logger.info("New request from {}".format(request.remote_addr))
    environment = request.args.get('env', type=str).upper()
    if not environment:
        return constants.ExceptionResponse.update(message="missing `env` argument"), constants.HTTP_400_BAD_REQUEST
    try:
        return get_active_namenode(environment)
    except Exception as e:
        logger.exception(e)
        return constants.ExceptionResponse.update(message=e), constants.HTTP_400_BAD_REQUEST
