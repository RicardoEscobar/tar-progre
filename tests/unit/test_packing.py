"""This module contains tests for the packing module."""

import unittest
from pathlib import Path

from tarprogre.controller.packing import pack


class TestPacking(unittest.TestCase):
    """Tests for the packing module."""

    def setUp(self) -> None:
        """Set up the tests."""
        # Create a temporary directory.
        self.source = Path("tests/data/source")
        self.source.mkdir(parents=True, exist_ok=True)

        # Create 1000 temporary files.
        for i in range(1000):
            file = self.source / f"file_{i}.txt"
            file.touch()

        # Create a temporary destination.
        self.destination = Path("tests/data/destination.tar")

    def tearDown(self) -> None:
        """Tear down the tests."""
        # Remove the temporary files.
        for file in self.source.rglob("*"):
            file.unlink()

        # Remove the temporary directory.
        self.source.rmdir()

        # Remove the temporary destination.
        self.destination.unlink()

        # Remove the temporary destination directory.
        self.destination.parent.rmdir()

    def test_pack(self):
        """Test the pack function."""
        # Pack the source directory.
        destination = pack(self.source, self.destination)

        # Check if the destination file exists.
        self.assertTrue(destination.exists())

        # Check if the destination file is a tarball.
        self.assertEqual(destination.suffix, ".tar")

        # Check if the destination file is not empty.
        self.assertTrue(destination.stat().st_size > 0)


if __name__ == "__main__":
    unittest.main()
