import logging

LOG_FORMAT = "%(levelname)s,%(asctime)s (%(threadName)s) [%(name)s] %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("optasia-api")