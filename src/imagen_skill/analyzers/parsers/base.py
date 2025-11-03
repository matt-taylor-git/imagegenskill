"""Base parser abstract class."""

from abc import ABC, abstractmethod
from pathlib import Path

from ...core.models import Opportunity


class BaseParser(ABC):
    """Abstract base class for code parsers."""

    @abstractmethod
    def find_opportunities(self, code: str, file_path: Path) -> list[Opportunity]:
        """Find UI enhancement opportunities in code.

        Args:
            code: Source code as string
            file_path: Path to the source file

        Returns:
            List of detected opportunities
        """
        pass

    def _extract_semantic(self, var_name: str) -> str:
        """Extract semantic meaning from variable name.

        Args:
            var_name: Variable name (e.g., "settingsButton", "profileIcon")

        Returns:
            Semantic context (e.g., "settings", "profile")
        """
        import re

        # Remove common suffixes
        semantic = re.sub(
            r"(Button|Icon|Pixmap|Label|Widget|Image|Sprite|Btn|Img)$",
            "",
            var_name,
            flags=re.IGNORECASE,
        )

        # Convert camelCase to lowercase with spaces
        semantic = re.sub(r"([A-Z])", r" \1", semantic).strip().lower()

        return semantic or "unknown"
