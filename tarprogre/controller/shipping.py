"""This module contains shipping a tarball through ssh functions using progress bar."""

from pathlib import Path
import getpass

import paramiko
from tqdm import tqdm

from tarprogre.controller.ssh_manager import get_ssh_client, create_remote_dir


def ship(client: paramiko.SSHClient, source: Path, destination: Path) -> Path:
    """Ship the source tarball to the destination host.
    Args:
        client: The ssh client.
        source: The source tarball.
        destination: The destination directory.
    Returns:
        The destination tarball.
    """
    # Create the sftp client.
    sftp = client.open_sftp()

    # Create the destination directory.
    create_remote_dir(client, destination.parent)

    # Create the progress bar.
    progress = tqdm(
        total=source.stat().st_size, unit="B", unit_scale=True, desc=source.name
    )

    # Ship the source tarball to the destination host.
    with sftp.file(destination.as_posix(), "wb") as file:
        with open(source, "rb") as source_file:
            for data in iter(lambda: source_file.read(10485760), b""):
                file.write(data)
                progress.update(len(data))

    # Close the sftp client.
    sftp.close()

    # Close the ssh client.
    client.close()

    return destination


def main():
    """Main function."""
    # Demo tarball shipping.
    source = Path("F:/FIRECUDA2/backup/WAIFUS/waifus.tar")
    # Destination path is posix path for the linux server.
    destination = Path("/home/jorge/waifus/waifus.tar")
    host = "192.168.1.253"
    user = "jorge"
    password = getpass.getpass("Password: ")
    # Create ssh client.
    client = get_ssh_client(host, user, password)
    # Ship the tarball to the destination host.
    ship(client, source, destination)


if __name__ == "__main__":
    main()
