"""This module contains packing functions using progress bar."""

import tarfile
from pathlib import Path

from tqdm import tqdm


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


if __name__ == "__main__":
    main()
