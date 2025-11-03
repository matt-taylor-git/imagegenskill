"""Base integrator abstract class."""

from abc import ABC, abstractmethod
from pathlib import Path

from ...core.models import Opportunity


class BaseIntegrator(ABC):
    """Abstract base class for code integrators."""

    @abstractmethod
    def integrate(self, code: str, opportunity: Opportunity, image_path: Path) -> str:
        """Integrate generated image into code.

        Args:
            code: Original source code
            opportunity: Opportunity object with location and context
            image_path: Path to generated image

        Returns:
            Updated source code with image integrated
        """
        pass

    def _to_resource_path(self, image_path: Path, project_root: Path | None = None) -> str:
        """Convert filesystem path to resource path.

        Args:
            image_path: Absolute path to image file
            project_root: Project root directory (optional)

        Returns:
            Resource path string
        """
        if project_root:
            try:
                rel_path = image_path.relative_to(project_root)
                return str(rel_path).replace("\\", "/")
            except ValueError:
                pass

        return str(image_path.name)
