"""Asset manager for organizing generated image files."""

import logging
from pathlib import Path

from ..core.models import Framework, ImagePurpose, Opportunity

logger = logging.getLogger("imagen_skill.asset_manager")


class AssetManager:
    """Manage asset file placement and naming."""

    # Framework-specific directory conventions
    DIRECTORY_CONVENTIONS = {
        Framework.QT: {
            ImagePurpose.ICON: "resources/icons",
            ImagePurpose.LOGO: "resources/images",
            ImagePurpose.BUTTON: "resources/ui/buttons",
            ImagePurpose.BACKGROUND: "resources/images/backgrounds",
            ImagePurpose.ILLUSTRATION: "resources/images",
            ImagePurpose.HERO: "resources/images",
        },
        Framework.REACT: {
            ImagePurpose.ICON: "src/assets/icons",
            ImagePurpose.LOGO: "src/assets/images",
            ImagePurpose.ILLUSTRATION: "src/assets/illustrations",
            ImagePurpose.HERO: "src/assets/images",
        },
        Framework.UNITY: {
            ImagePurpose.ICON: "Assets/Resources/UI/Icons",
            ImagePurpose.LOGO: "Assets/Resources/UI",
            ImagePurpose.BACKGROUND: "Assets/Resources/Backgrounds",
        },
        Framework.HTML: {
            ImagePurpose.ICON: "assets/icons",
            ImagePurpose.LOGO: "assets/images",
            ImagePurpose.BACKGROUND: "assets/images",
        },
    }

    def determine_save_path(self, opportunity: Opportunity, project_root: Path) -> Path:
        """Determine where to save generated image.

        Args:
            opportunity: Opportunity with framework and purpose
            project_root: Project root directory

        Returns:
            Full path where image should be saved
        """
        # Get conventional directory
        convention = self.DIRECTORY_CONVENTIONS.get(opportunity.framework, {})
        relative_dir = convention.get(opportunity.purpose, "resources/images")  # Default fallback

        full_dir = project_root / relative_dir

        # Create directory if it doesn't exist
        full_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        filename = self._generate_filename(opportunity)

        # Handle conflicts
        full_path = full_dir / filename
        full_path = self._handle_conflict(full_path)

        logger.info(f"Determined save path: {full_path}")

        return full_path

    def _generate_filename(self, opportunity: Opportunity) -> str:
        """Generate semantic filename from opportunity.

        Args:
            opportunity: Opportunity with semantic context and purpose

        Returns:
            Filename (e.g., "settings-icon.png")
        """
        # Sanitize semantic context
        base = opportunity.semantic_context.lower().replace(" ", "-")
        base = "".join(c for c in base if c.isalnum() or c == "-")

        # Add purpose suffix
        suffix_map = {
            ImagePurpose.ICON: "-icon",
            ImagePurpose.LOGO: "-logo",
            ImagePurpose.BUTTON: "-button",
            ImagePurpose.BACKGROUND: "-bg",
            ImagePurpose.ILLUSTRATION: "-illust",
            ImagePurpose.HERO: "-hero",
        }
        suffix = suffix_map.get(opportunity.purpose, "")

        return f"{base}{suffix}.png"

    def _handle_conflict(self, path: Path) -> Path:
        """Handle filename conflicts by appending numbers.

        Args:
            path: Desired file path

        Returns:
            Available file path (may have number appended)
        """
        if not path.exists():
            return path

        # Append numbers until we find an available name
        stem = path.stem
        suffix = path.suffix
        parent = path.parent
        counter = 1

        while True:
            new_path = parent / f"{stem}-{counter}{suffix}"
            if not new_path.exists():
                logger.debug(f"Resolved conflict: {path.name} -> {new_path.name}")
                return new_path
            counter += 1

            if counter > 100:  # Safety limit
                raise ValueError(f"Too many conflicts for: {path}")
