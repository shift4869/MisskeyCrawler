import logging.config
from logging import INFO, getLogger

logging.config.fileConfig("./log/logging.ini", disable_existing_loggers=False)
logger = getLogger(__name__)
logger.setLevel(INFO)
