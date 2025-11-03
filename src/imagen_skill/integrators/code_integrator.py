"""Code integrator for updating source files with generated images."""

import difflib
import logging
from pathlib import Path

from ..core.models import (
    Framework,
    GeneratedImage,
    IntegrationResult,
)
from ..exceptions import IntegrationError
from ..utils.file_utils import read_file_async, write_file_async
from .frameworks.base import BaseIntegrator
from .frameworks.qt_integrator import QtIntegrator

logger = logging.getLogger("imagen_skill.code_integrator")


class CodeIntegrator:
    """Integrate generated images into code files."""

    def __init__(self) -> None:
        """Initialize code integrator with available framework integrators."""
        self.integrators: dict[Framework, BaseIntegrator] = {
            Framework.QT: QtIntegrator(),
            # Future: React, Unity, HTML integrators
        }

    async def integrate(
        self,
        generated_image: GeneratedImage,
        project_root: Path,
        dry_run: bool = False,
    ) -> IntegrationResult:
        """Integrate generated image into code.

        Args:
            generated_image: Generated image with opportunity metadata
            project_root: Project root directory
            dry_run: If True, generate diff without applying changes

        Returns:
            IntegrationResult with success status and diff

        Raises:
            IntegrationError: If integration fails
        """
        opportunity = generated_image.opportunity
        file_path = opportunity.location.file_path

        try:
            # Read current code
            code = await read_file_async(file_path)

            # Get appropriate integrator
            integrator = self.integrators.get(opportunity.framework)
            if integrator is None:
                raise IntegrationError(f"No integrator available for {opportunity.framework}")

            # Generate updated code
            logger.info(
                f"Integrating into {file_path.name} at line {opportunity.location.line_number}"
            )
            updated_code = integrator.integrate(
                code=code,
                opportunity=opportunity,
                image_path=generated_image.file_path,
            )

            # Validate syntax (basic check - just ensure it's not empty)
            if not updated_code.strip():
                raise IntegrationError("Generated code is empty")

            # Generate diff
            diff = self._generate_diff(code, updated_code, file_path)

            if dry_run:
                logger.info("Dry run - changes not applied")
                return IntegrationResult(
                    success=True,
                    file_path=file_path,
                    diff=diff,
                )

            # Apply changes
            await write_file_async(file_path, updated_code)

            # Handle framework-specific resource files
            if opportunity.framework == Framework.QT:
                await self._update_qt_resources(generated_image, project_root, integrator)

            logger.info(f"Successfully integrated into {file_path.name}")

            return IntegrationResult(
                success=True,
                file_path=file_path,
                diff=diff,
            )

        except Exception as e:
            error_msg = f"Integration failed for {file_path.name}: {e}"
            logger.error(error_msg)
            return IntegrationResult(
                success=False,
                file_path=file_path,
                diff="",
                error=str(e),
            )

    def _generate_diff(self, original: str, updated: str, file_path: Path) -> str:
        """Generate unified diff between original and updated code.

        Args:
            original: Original code
            updated: Updated code
            file_path: File path for diff headers

        Returns:
            Unified diff string
        """
        diff_lines = difflib.unified_diff(
            original.splitlines(keepends=True),
            updated.splitlines(keepends=True),
            fromfile=f"a/{file_path.name}",
            tofile=f"b/{file_path.name}",
            lineterm="",
        )

        return "".join(diff_lines)

    async def _update_qt_resources(
        self,
        generated_image: GeneratedImage,
        project_root: Path,
        integrator: BaseIntegrator,
    ) -> None:
        """Update Qt .qrc resource file.

        Args:
            generated_image: Generated image metadata
            project_root: Project root directory
            integrator: Qt integrator instance
        """
        # Look for .qrc file in project
        qrc_files = list(project_root.glob("*.qrc"))

        if not qrc_files:
            # Create default resources.qrc
            qrc_path = project_root / "resources.qrc"
            logger.info(f"Creating new .qrc file: {qrc_path}")
        else:
            qrc_path = qrc_files[0]
            logger.info(f"Updating existing .qrc file: {qrc_path}")

        # Calculate relative path from project root
        try:
            rel_path = generated_image.file_path.relative_to(project_root)
        except ValueError:
            logger.warning(f"Image path {generated_image.file_path} not under project root")
            return

        # Update .qrc file
        if isinstance(integrator, QtIntegrator):
            integrator.update_qrc_file(qrc_path, rel_path)
