from remotely.remote_ssh import SSHClient
from remotely.remotely_logger import logger_main
from remotely.remotely_app import app

logger = logger_main.Logger(__name__).logger


def run():
    app.app.run_server(debug=True)
