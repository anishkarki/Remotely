import logging
import sys


class Logger:
    """
    A class that creates a logger object which can be used to log messages.

    The logger can output messages to both a file and the console, with a detailed formatter.

    :param log_file: The path to the log file to use. Defaults to 'log.txt'.
    :type log_file: str
    :param log_level: The minimum log level to output. Defaults to logging.DEBUG.
    :type log_level: int
    """

    def __init__(self,name, log_file='/tmp/remotelylog.log', log_level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Create a file handler and add it to the logger
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(file_handler)

        # Create a console handler and add it to the logger
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(console_handler)

    def _get_formatter(self):
        """
        Returns a detailed log formatter with module name, function name, line number and timestamp.
        """
        return logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(module)s.%(funcName)s:%(lineno)d - %(message)s')
