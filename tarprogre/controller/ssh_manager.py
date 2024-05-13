"""This module contains functions to create connections to the server and manage files remotely."""
from pathlib import Path

import paramiko


def get_ssh_client(host: str, user: str, password: str) -> paramiko.SSHClient:
    """Get an ssh connection to the host.
    Args:
        host: The destination host.
        user: The destination user.
        password: The destination password.
    Returns:
        The ssh connection.
    """
    # Create the ssh client.
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=password)
    return client


def create_remote_dir(connection: paramiko.SSHClient, remote_dir: Path):
    """Create a remote directory on the server."""
    sftp = connection.open_sftp()
    try:
        sftp.mkdir(remote_dir.as_posix(), mode=0o755)
    except IOError:
        pass
    sftp.close()