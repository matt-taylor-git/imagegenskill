"""File operation utilities."""

from pathlib import Path

import aiofiles

from ..exceptions import FileOperationError


async def read_file_async(file_path: Path) -> str:
    """Read file contents asynchronously.

    Args:
        file_path: Path to file

    Returns:
        File contents as string

    Raises:
        FileOperationError: If file cannot be read
    """
    try:
        async with aiofiles.open(file_path, encoding="utf-8") as f:
            content: str = await f.read()  # type: ignore[assignment]
            return content
    except Exception as e:
        raise FileOperationError(f"Failed to read file {file_path}: {e}") from e


async def write_file_async(file_path: Path, content: str) -> None:
    """Write content to file asynchronously.

    Args:
        file_path: Path to file
        content: Content to write

    Raises:
        FileOperationError: If file cannot be written
    """
    try:
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
            await f.write(content)
    except Exception as e:
        raise FileOperationError(f"Failed to write file {file_path}: {e}") from e


async def write_bytes_async(file_path: Path, content: bytes) -> None:
    """Write binary content to file asynchronously.

    Args:
        file_path: Path to file
        content: Binary content to write

    Raises:
        FileOperationError: If file cannot be written
    """
    try:
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)
    except Exception as e:
        raise FileOperationError(f"Failed to write binary file {file_path}: {e}") from e
