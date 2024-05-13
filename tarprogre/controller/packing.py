"""This module contains packing functions using progress bar."""

import tarfile
from pathlib import Path
import getpass

from tqdm import tqdm
from paramiko import SSHClient

from tarprogre.controller.ssh_manager import get_ssh_client, create_remote_dir


def pack(source: Path, destination: Path) -> Path:
    """Pack the source directory into a tarball.
    Args:
        source: The directory to pack.
        destination: The destination tarball.
    Returns:
        The destination tarball.
    """
    # Create the destination directory.
    destination.parent.mkdir(parents=True, exist_ok=True)

    with tarfile.open(destination, "w") as tar:
        files = list(source.rglob("*"))
        for file in tqdm(files, unit="files"):
            tar.add(file, arcname=file.relative_to(source))
    return destination


def unpack_tar(client: SSHClient, source: Path, destination: Path) -> Path:
    """Unpack the source tarball into the destination directory.
    Args:
        source: The source tarball.
        destination: The destination directory.
    Returns:
        The destination directory.
    """
    # Create the destination directory.
    create_remote_dir(client, destination)

    # Create the sftp client.
    sftp = client.open_sftp()

    # Create the progress bar.
    progress = tqdm(
        total=source.stat().st_size, unit="B", unit_scale=True, desc=source.name
    )

    # Unpack the source tarball into the destination directory.
    with sftp.file(source.as_posix(), "rb") as file:
        with tarfile.open(fileobj=file, mode="r|") as tar:
            for member in tar:
                tar.extract(member, destination)
                progress.update(tar.offset)


def main():
    """Main function."""
    # Demo tarball packing.
    source = Path("F:/FIRECUDA2/backup/WAIFUS")
    destination = Path("F:/FIRECUDA2/backup/WAIFUS/waifus.tar")
    # Pack jpeg files into a tarball.
    with tarfile.open(destination, "w") as tar:
        files = list(source.rglob("*.jpg"))
        for file in tqdm(files, unit="files"):
            tar.add(file, arcname=file.relative_to(source))


def main2():
    """Main function."""
    # Demo tarball unpacking.
    source = Path("/home/jorge/waifus/waifus.tar")
    destination = Path("/home/jorge/waifus")
    host = "192.168.1.253"
    user = "jorge"
    password = getpass.getpass("Password: ")
    # Create ssh client.
    client = get_ssh_client(host, user, password)
    # Unpack the tarball to the destination directory.
    unpack_tar(client, source, destination)


if __name__ == "__main__":
    main2()
