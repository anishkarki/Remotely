import paramiko
import pytest

from remotely.remote_ssh import SSHClient


@pytest.fixture
def ssh_client():
    client = SSHClient("localhost", "testuser", "testpass")
    client.connect()
    yield client
    client.close()


def test_ssh_connect(ssh_client):
    assert isinstance(SSHClient, paramiko.SSHClient)


@pytest.fixture
def test_execute_command():
    # Set up an SSH connection
    client = SSHClient("remote.server.com", "username", "password")
    client.connect()

    # Execute a command
    output, error = client.execute_command("ls")

    # Check that the command was executed successfully
    assert error == "", f"Error message: {error}"
    assert output != "", "Output is empty"

    # Close the SSH connection
    client.close()


@pytest.fixture
def test_execute_commands_in_parallel():
    # Set up an SSH connection
    client = SSHClient("remote.server.com", "username", "password")
    client.connect()

    # Execute multiple commands in parallel
    commands = ["ls", "pwd", 'echo "Hello world!"']
    results = client.execute_commands_in_parallel(commands)

    # Check that the commands were executed successfully
    assert len(results) == len(commands), "Incorrect number of results"
    for result in results:
        output, error = result
        assert error == "", f"Error message: {error}"
        assert output != "", "Output is empty"

    # Close the SSH connection
    client.close()
