import logging

logging.basicConfig()
_logger = logging.getLogger(__name__)

_logger.setLevel(logging.INFO)
if __debug__:
    _logger.setLevel(logging.DEBUG)
