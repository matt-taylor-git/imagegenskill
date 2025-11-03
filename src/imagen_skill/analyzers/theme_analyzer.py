"""Theme analyzer for extracting visual properties from reference images."""

import logging
from pathlib import Path

from ..core.models import ColorPalette, ThemeProfile, VisualStyle
from ..exceptions import ThemeAnalysisError
from ..services.gemini_client import GeminiClient

logger = logging.getLogger("imagen_skill.theme_analyzer")


class ThemeAnalyzer:
    """Extract visual theme from reference images using Gemini Vision."""

    def __init__(self, gemini_client: GeminiClient):
        """Initialize theme analyzer.

        Args:
            gemini_client: Configured Gemini client for API calls
        """
        self.client = gemini_client

    async def analyze(self, image_path: Path) -> ThemeProfile:
        """Analyze theme from reference image.

        Args:
            image_path: Path to reference image

        Returns:
            ThemeProfile with extracted colors, style, and patterns

        Raises:
            ThemeAnalysisError: If analysis fails
        """
        logger.info(f"Analyzing theme from: {image_path}")

        prompt = """
        Analyze this UI design/screenshot and extract theme information.

        Return JSON with this exact structure:
        {
            "colors": {
                "primary": "#RRGGBB",
                "secondary": ["#RRGGBB", "#RRGGBB"],
                "accent": ["#RRGGBB"],
                "background": "#RRGGBB",
                "text": "#RRGGBB"
            },
            "style": {
                "aesthetic": "modern minimal|retro|playful|professional|etc",
                "mood": "serious|playful|elegant|technical|etc",
                "keywords": ["clean", "rounded", "shadow"],
                "icon_style": "outline|filled|flat|3d|null"
            },
            "patterns": ["rounded corners", "drop shadows", "gradients"]
        }

        Extract:
        1. Primary color (most dominant UI color)
        2. Secondary colors (2-3 supporting colors)
        3. Accent colors (1-2 highlighting colors)
        4. Background color (main background)
        5. Text color (main text color)
        6. Aesthetic description (e.g., "modern minimal", "vibrant playful")
        7. Overall mood (professional, casual, technical, etc.)
        8. Visual keywords (clean, rounded, shadowed, flat, etc.)
        9. Icon style if icons are visible
        10. Common patterns (rounded corners, shadows, gradients, etc.)

        All colors must be valid hex codes starting with #.
        """

        try:
            theme_data = await self.client.analyze_image_vision(image_path, prompt)

            # Validate and parse into ThemeProfile
            theme_profile = ThemeProfile(
                colors=ColorPalette(**theme_data["colors"]),
                style=VisualStyle(**theme_data["style"]),
                patterns=theme_data.get("patterns", []),
                source_image=str(image_path),
            )

            logger.info(
                f"Theme extracted: {theme_profile.style.aesthetic}, "
                f"primary={theme_profile.colors.primary}"
            )

            return theme_profile

        except KeyError as e:
            raise ThemeAnalysisError(f"Invalid theme data structure, missing key: {e}") from e
        except Exception as e:
            raise ThemeAnalysisError(f"Theme analysis failed: {e}") from e
