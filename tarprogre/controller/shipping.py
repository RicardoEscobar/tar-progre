"""This module contains shipping a tarball through ssh functions using progress bar."""

from pathlib import Path
import getpass

import paramiko
from tqdm import tqdm


def ship(source: Path, destination: Path, host: str, user: str, password: str) -> Path:
    """Ship the source tarball to the destination host.
    Args:
        source: The source tarball.
        destination: The destination directory.
        host: The destination host.
        user: The destination user.
        password: The destination password.
    Returns:
        The destination tarball.
    """
    # Create the ssh client.
    client = get_ssh_client(host, user, password)

    # Create the sftp client.
    sftp = client.open_sftp()

    # Create the destination directory.
    sftp.mkdir(str(destination.parent), mode=0o755)

    # Create the progress bar.
    progress = tqdm(
        total=source.stat().st_size, unit="B", unit_scale=True, desc=source.name
    )

    # Ship the source tarball to the destination host.
    with sftp.file(str(destination), "wb") as file:
        with open(source, "rb") as source_file:
            for data in iter(lambda: source_file.read(10485760), b""):
                file.write(data)
                progress.update(len(data))

    # Close the sftp client.
    sftp.close()

    # Close the ssh client.
    client.close()

    return destination


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


def main():
    """Main function."""
    # Demo tarball shipping.
    source = Path("F:/FIRECUDA2/backup/WAIFUS/waifus.tar")
    # Destination path is posix path for the linux server.
    destination = Path("home\\jorge\\waifus.tar")
    host = "192.168.1.253"
    user = "jorge"
    password = getpass.getpass("Password: ")
    # Ship the tarball to the destination host.
    ship(source, destination, host, user, password)


if __name__ == "__main__":
    main()
