from remotely.remote_ssh import SSHClient
from remotely.remotely_logger import logger_main

logger = logger_main.Logger(__name__).logger

def run():
    logger.debug('running..')