"""Type definitions, aliases, and protocols."""

from pathlib import Path
from typing import Protocol, runtime_checkable

# Type aliases for clarity
FilePath = Path | str
ImageBytes = bytes
PromptText = str
HexColor = str  # e.g., "#7C3AED"


@runtime_checkable
class Parser(Protocol):
    """Protocol for code parsers."""

    def find_opportunities(self, code: str, file_path: Path) -> list[object]:
        """Find UI enhancement opportunities in code.

        Args:
            code: Source code as string
            file_path: Path to the source file

        Returns:
            List of Opportunity objects
        """
        ...


@runtime_checkable
class Integrator(Protocol):
    """Protocol for code integrators."""

    def integrate(self, code: str, opportunity: object, image_path: Path) -> str:
        """Integrate generated image into code.

        Args:
            code: Original source code
            opportunity: Opportunity object with location and context
            image_path: Path to generated image

        Returns:
            Updated source code with image integrated
        """
        ...
