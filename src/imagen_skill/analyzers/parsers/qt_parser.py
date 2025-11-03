"""Qt C++ code parser for finding UI enhancement opportunities."""

import logging
from pathlib import Path

from ...core.models import (
    CodeLocation,
    Framework,
    ImagePurpose,
    IntegrationType,
    Opportunity,
)
from .base import BaseParser
from .patterns import QT_PATTERNS

logger = logging.getLogger("imagen_skill.qt_parser")


class QtCodeParser(BaseParser):
    """Parse Qt C++ code to find image opportunities."""

    def find_opportunities(self, code: str, file_path: Path) -> list[Opportunity]:
        """Find UI enhancement opportunities in Qt C++ code.

        Args:
            code: Source code as string
            file_path: Path to the source file

        Returns:
            List of detected opportunities
        """
        opportunities: list[Opportunity] = []

        # Pattern 1: button.setIcon(QIcon())
        for match in QT_PATTERNS["empty_qicon"].finditer(code):
            var_name = match.group(1)
            line_num = code[: match.start()].count("\n") + 1
            semantic = self._extract_semantic(var_name)

            opportunities.append(
                Opportunity(
                    location=CodeLocation(file_path=file_path, line_number=line_num),
                    purpose=ImagePurpose.ICON,
                    semantic_context=semantic,
                    code_snippet=match.group(0),
                    integration_type=IntegrationType.QT_ICON,
                    confidence=0.9,  # High confidence for explicit QIcon()
                    size_hint="32x32",  # Default icon size
                    framework=Framework.QT,
                )
            )

        # Pattern 2: QIcon("")
        for match in QT_PATTERNS["empty_qicon_string"].finditer(code):
            line_num = code[: match.start()].count("\n") + 1

            # Try to find variable context nearby
            line_start = code.rfind("\n", 0, match.start()) + 1
            line_end = code.find("\n", match.end())
            if line_end == -1:
                line_end = len(code)
            line_text = code[line_start:line_end]

            # Extract variable name if available
            var_match = __import__("re").search(r"(\w+)\s*[=.]", line_text)
            semantic = self._extract_semantic(var_match.group(1)) if var_match else "icon"

            opportunities.append(
                Opportunity(
                    location=CodeLocation(file_path=file_path, line_number=line_num),
                    purpose=ImagePurpose.ICON,
                    semantic_context=semantic,
                    code_snippet=match.group(0),
                    integration_type=IntegrationType.QT_ICON,
                    confidence=0.85,
                    size_hint="32x32",
                    framework=Framework.QT,
                )
            )

        # Pattern 3: setWindowIcon(QIcon())
        for match in QT_PATTERNS["window_icon"].finditer(code):
            line_num = code[: match.start()].count("\n") + 1

            opportunities.append(
                Opportunity(
                    location=CodeLocation(file_path=file_path, line_number=line_num),
                    purpose=ImagePurpose.LOGO,
                    semantic_context="application window",
                    code_snippet=match.group(0),
                    integration_type=IntegrationType.QT_ICON,
                    confidence=0.95,
                    size_hint="64x64",  # Window icons typically larger
                    framework=Framework.QT,
                )
            )

        # Pattern 4: QPixmap pixmap;
        for match in QT_PATTERNS["empty_qpixmap"].finditer(code):
            var_name = match.group(1)
            line_num = code[: match.start()].count("\n") + 1
            semantic = self._extract_semantic(var_name)

            # Determine purpose based on variable name
            purpose = ImagePurpose.LOGO
            if "background" in var_name.lower() or "bg" in var_name.lower():
                purpose = ImagePurpose.BACKGROUND
            elif "hero" in var_name.lower():
                purpose = ImagePurpose.HERO

            opportunities.append(
                Opportunity(
                    location=CodeLocation(file_path=file_path, line_number=line_num),
                    purpose=purpose,
                    semantic_context=semantic,
                    code_snippet=match.group(0),
                    integration_type=IntegrationType.QT_PIXMAP,
                    confidence=0.7,  # Medium confidence - could be intentional
                    size_hint=None,
                    framework=Framework.QT,
                )
            )

        # Pattern 5: Placeholder paths
        for match in QT_PATTERNS["placeholder_path"].finditer(code):
            line_num = code[: match.start()].count("\n") + 1

            # Try to extract variable context
            line_start = code.rfind("\n", 0, match.start()) + 1
            line_text = code[line_start : match.end() + 50]
            var_match = __import__("re").search(r"(\w+)\s*(?:\(|=)", line_text)
            semantic = self._extract_semantic(var_match.group(1)) if var_match else "placeholder"

            opportunities.append(
                Opportunity(
                    location=CodeLocation(file_path=file_path, line_number=line_num),
                    purpose=ImagePurpose.ILLUSTRATION,
                    semantic_context=semantic,
                    code_snippet=match.group(0),
                    integration_type=IntegrationType.QT_PIXMAP,
                    confidence=0.95,  # High confidence - explicitly marked placeholder
                    size_hint=None,
                    framework=Framework.QT,
                )
            )

        logger.info(f"Found {len(opportunities)} opportunities in {file_path.name} (Qt)")
        return opportunities
