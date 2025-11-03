"""Code analyzer for detecting UI enhancement opportunities."""

import logging
from pathlib import Path

from ..core.models import Framework, Opportunity
from ..exceptions import ParsingError
from .parsers.base import BaseParser
from .parsers.qt_parser import QtCodeParser

logger = logging.getLogger("imagen_skill.code_analyzer")


class CodeAnalyzer:
    """Analyze code files to find UI enhancement opportunities."""

    def __init__(self) -> None:
        """Initialize code analyzer with available parsers."""
        self.parsers: dict[Framework, BaseParser] = {
            Framework.QT: QtCodeParser(),
            # Future: React, Unity, HTML parsers
        }

    def detect_framework(self, file_path: Path, code: str) -> Framework | None:
        """Detect framework from file extension and content.

        Args:
            file_path: Path to source file
            code: Source code content

        Returns:
            Detected framework or None
        """
        suffix = file_path.suffix.lower()

        # Qt C++
        if suffix in [".cpp", ".h", ".hpp", ".cc"]:
            # Check for Qt-specific patterns
            if any(
                pattern in code for pattern in ["#include <Q", "QWidget", "QApplication", "QIcon"]
            ):
                return Framework.QT

        # React
        elif suffix in [".jsx", ".tsx"]:
            if "import React" in code or "from 'react'" in code:
                return Framework.REACT

        # Unity C#
        elif suffix == ".cs":
            if "UnityEngine" in code or "MonoBehaviour" in code:
                return Framework.UNITY

        # HTML
        elif suffix in [".html", ".htm"]:
            return Framework.HTML

        return None

    async def analyze(
        self, file_paths: list[Path], _project_root: Path | None = None
    ) -> list[Opportunity]:
        """Analyze code files for UI enhancement opportunities.

        Args:
            file_paths: List of source file paths to analyze
            project_root: Project root directory (optional)

        Returns:
            List of detected opportunities, sorted by confidence

        Raises:
            ParsingError: If file cannot be read or parsed
        """
        all_opportunities: list[Opportunity] = []

        for file_path in file_paths:
            try:
                # Read file
                code = file_path.read_text(encoding="utf-8")

                # Detect framework
                framework = self.detect_framework(file_path, code)

                if framework is None:
                    logger.warning(f"Could not detect framework for {file_path}")
                    continue

                # Get appropriate parser
                parser = self.parsers.get(framework)
                if parser is None:
                    logger.warning(f"No parser available for {framework}")
                    continue

                # Parse and find opportunities
                opportunities = parser.find_opportunities(code, file_path)
                all_opportunities.extend(opportunities)

                logger.info(f"Analyzed {file_path.name}: {len(opportunities)} opportunities found")

            except Exception as e:
                raise ParsingError(f"Failed to analyze {file_path}: {e}") from e

        # Sort by confidence (highest first)
        all_opportunities.sort(key=lambda opp: opp.confidence, reverse=True)

        logger.info(
            f"Total opportunities found: {len(all_opportunities)} across {len(file_paths)} files"
        )

        return all_opportunities
