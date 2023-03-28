import paramiko
import concurrent.futures
from remotely.remotely_logger import logger_main

logger = logger_main.Logger(__name__).logger

class SSHClient:
    """
    A class for making SSH connections and executing remote commands.

    :param hostname: The hostname or IP address of the remote server.
    :type hostname: str
    :param username: The username to use for the SSH connection.
    :type username: str
    :param password: The password to use for the SSH connection.
    :type password: str

    :raises paramiko.ssh_exception.AuthenticationException: If the authentication fails.

    Example usage:

    >>> client = SSHClient('remote.server.com', 'username', 'password')
    >>> client.connect()
    >>> output, error = client.execute_command('ls')
    >>> print(output)
    >>> client.close()
    """

    def __init__(self, hostname, username, password):
        """
        Initializes a new SSHClient object.

        :param hostname: The hostname or IP address of the remote server.
        :type hostname: str
        :param username: The username to use for the SSH connection.
        :type username: str
        :param password: The password to use for the SSH connection.
        :type password: str

        :raises paramiko.ssh_exception.AuthenticationException: If the authentication fails.
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        """
        Connects to the remote server.

        :raises paramiko.ssh_exception.AuthenticationException: If the authentication fails.
        """
        try:
            self.client.connect(hostname=self.hostname, username=self.username, password=self.password)
        except paramiko.ssh_exception.AuthenticationException as e:
            logger.error(f"Failed to connect to {self.hostname}: {str(e)}")
            raise e
    def execute_command(self, command):
        """
        Executes a command on the remote server.

        :param command: The command to execute.
        :type command: str

        :return: A tuple containing the standard output and standard error streams from the command.
        :rtype: tuple(str, str)
        """
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            return stdout.read().decode(), stderr.read().decode()
        except Exception as e:
            logger.error(f"Failed to execute command {command}: {str(e)}")
            raise e

    def run_command_with_input(self, command, input_str):
        try:
            channel = self.client.invoke_shell()
            channel.send(command + '\n')
            while not channel.recv_ready():
                continue
            output = channel.recv(1024).decode('utf-8')
            print(output)
            channel.send(input_str + '\n')
            while not channel.recv_ready():
                continue
            output = channel.recv(1024).decode('utf-8')
            print(output)
            channel.close()
        except Exception as e:
            logger.error(f"Failed to run command with input {command}: {str(e)}")
            raise e

    def execute_commands_in_parallel(self, commands):
        """
        Executes a list of commands in parallel using multiple threads.

        :param commands: The list of commands to execute.
        :type commands: List[str]

        :return: A list of tuples containing the standard output and standard error streams from each command.
        :rtype: List[tuple(str, str)]
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit each command to the executor as a separate task
            futures = [executor.submit(self.execute_command, cmd) for cmd in commands]
            # Wait for all tasks to complete and retrieve their results
            results = [future.result() for future in futures]
            return results

    def get_current_user(self):
        stdin, stdout, stderr = self.client.exec_command('whoami')
        output = stdout.read().decode('utf-8').strip()
        return output

    def close(self):
        """
        Closes the SSH connection.
        """
        self.client.close()