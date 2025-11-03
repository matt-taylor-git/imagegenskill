"""Qt C++ code integrator."""

import logging
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from ...core.models import IntegrationType, Opportunity
from ...exceptions import IntegrationError
from .base import BaseIntegrator

logger = logging.getLogger("imagen_skill.qt_integrator")


class QtIntegrator(BaseIntegrator):
    """Integrate images into Qt C++ code."""

    def integrate(self, code: str, opportunity: Opportunity, image_path: Path) -> str:
        """Update Qt code with image reference.

        Args:
            code: Original source code
            opportunity: Opportunity with location and integration type
            image_path: Path to generated image

        Returns:
            Updated source code

        Raises:
            IntegrationError: If integration fails
        """
        try:
            lines = code.split("\n")

            if opportunity.location.line_number > len(lines):
                raise IntegrationError(
                    f"Line number {opportunity.location.line_number} exceeds file length"
                )

            target_line_idx = opportunity.location.line_number - 1
            target_line = lines[target_line_idx]

            # Convert to Qt resource path
            resource_path = self._to_qt_resource_path(image_path)

            # Apply integration based on type
            if opportunity.integration_type == IntegrationType.QT_ICON:
                updated_line = self._integrate_qicon(target_line, resource_path)
            elif opportunity.integration_type == IntegrationType.QT_PIXMAP:
                updated_line = self._integrate_qpixmap(target_line, resource_path)
            else:
                raise IntegrationError(
                    f"Unsupported integration type: {opportunity.integration_type}"
                )

            lines[target_line_idx] = updated_line

            logger.info(
                f"Integrated image at line {opportunity.location.line_number}: {resource_path}"
            )

            return "\n".join(lines)

        except Exception as e:
            raise IntegrationError(f"Qt integration failed: {e}") from e

    def _integrate_qicon(self, line: str, resource_path: str) -> str:
        """Integrate QIcon with resource path.

        Args:
            line: Original line of code
            resource_path: Qt resource path

        Returns:
            Updated line
        """
        # Replace: QIcon() -> QIcon(":/path/to/resource.png")
        updated = re.sub(
            r"QIcon\s*\(\s*\)",
            f'QIcon("{resource_path}")',
            line,
        )

        # Also handle QIcon("")
        updated = re.sub(
            r'QIcon\s*\(\s*["\']["\']\s*\)',
            f'QIcon("{resource_path}")',
            updated,
        )

        return updated

    def _integrate_qpixmap(self, line: str, resource_path: str) -> str:
        """Integrate QPixmap with resource path.

        Args:
            line: Original line of code
            resource_path: Qt resource path

        Returns:
            Updated line
        """
        # Replace: QPixmap varname; -> QPixmap varname(":/path");
        updated = re.sub(
            r"(QPixmap\s+\w+)\s*;",
            f'\\1("{resource_path}");',
            line,
        )

        # Replace: QPixmap("placeholder") -> QPixmap(":/path")
        updated = re.sub(
            r'QPixmap\s*\(["\'](?:placeholder|temp|todo|empty)["\']\)',
            f'QPixmap("{resource_path}")',
            updated,
        )

        return updated

    def _to_qt_resource_path(self, image_path: Path) -> str:
        """Convert file path to Qt resource path.

        Args:
            image_path: Filesystem path to image

        Returns:
            Qt resource path (e.g., ":/resources/icons/settings.png")
        """
        # Extract relative path from common Qt structure
        parts = image_path.parts

        # Find 'resources' in path or use from first directory
        try:
            res_idx = parts.index("resources")
            rel_path = "/".join(parts[res_idx:])
        except ValueError:
            # If no 'resources' directory, use filename
            rel_path = f"resources/{image_path.name}"

        return f":/{rel_path}"

    def update_qrc_file(self, qrc_path: Path, resource_path: Path) -> None:
        """Add resource entry to Qt .qrc file.

        Args:
            qrc_path: Path to .qrc file
            resource_path: Relative path to resource file

        Raises:
            IntegrationError: If .qrc update fails
        """
        try:
            # Parse existing .qrc file or create new structure
            if qrc_path.exists():
                tree = ET.parse(qrc_path)
                root = tree.getroot()
            else:
                root = ET.Element("RCC")
                tree = ET.ElementTree(root)

            # Find or create qresource element
            qresource = root.find("qresource")
            if qresource is None:
                qresource = ET.SubElement(root, "qresource", prefix="/")

            # Check if file already exists
            resource_str = str(resource_path).replace("\\", "/")
            for file_elem in qresource.findall("file"):
                if file_elem.text == resource_str:
                    logger.info(f"Resource already in .qrc: {resource_str}")
                    return

            # Add file entry
            file_elem = ET.SubElement(qresource, "file")
            file_elem.text = resource_str

            # Write back
            tree.write(qrc_path, encoding="utf-8", xml_declaration=True)

            logger.info(f"Added to .qrc: {resource_str}")

        except Exception as e:
            raise IntegrationError(f"Failed to update .qrc file: {e}") from e
