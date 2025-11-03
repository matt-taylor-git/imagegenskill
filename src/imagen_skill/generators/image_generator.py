"""Image generator orchestrating prompt building, generation, and background removal."""

import logging
from pathlib import Path

from ..core.models import GeneratedImage, Opportunity, ThemeProfile
from ..exceptions import ImageGenerationError
from ..services.gemini_client import GeminiClient
from ..utils.file_utils import write_bytes_async
from .background_remover import BackgroundRemover
from .prompt_builder import PromptBuilder

logger = logging.getLogger("imagen_skill.image_generator")


class ImageGenerator:
    """Generate images using Imagen API with theme consistency."""

    # Estimated costs (USD per image)
    IMAGEN_COST_PER_IMAGE = 0.03

    def __init__(
        self,
        gemini_client: GeminiClient,
        prompt_builder: PromptBuilder,
        background_remover: BackgroundRemover,
    ):
        """Initialize image generator.

        Args:
            gemini_client: Gemini client for API calls
            prompt_builder: Prompt builder for creating generation prompts
            background_remover: Background remover for transparent images
        """
        self.client = gemini_client
        self.prompt_builder = prompt_builder
        self.background_remover = background_remover

    async def generate(
        self,
        opportunity: Opportunity,
        theme: ThemeProfile,
        output_dir: Path,
    ) -> GeneratedImage:
        """Generate image for specific opportunity.

        Args:
            opportunity: Opportunity with context and location
            theme: Theme profile for consistent styling
            output_dir: Directory to save generated image

        Returns:
            GeneratedImage with metadata

        Raises:
            ImageGenerationError: If generation fails
        """
        try:
            # Build prompt
            prompt = self.prompt_builder.build_prompt(opportunity, theme)
            aspect_ratio = self.prompt_builder.determine_aspect_ratio(opportunity)

            logger.info(
                f"Generating {opportunity.purpose.value} for '{opportunity.semantic_context}'"
            )
            logger.debug(f"Prompt: {prompt}")
            logger.debug(f"Aspect ratio: {aspect_ratio}")

            # Generate image
            image_bytes = await self.client.generate_image(
                prompt=prompt,
                aspect_ratio=aspect_ratio,
                number_of_images=1,
            )

            # Remove background if needed
            if opportunity.purpose.value in ["icon", "logo"]:
                logger.info("Removing background...")
                image_bytes = await self.background_remover.remove(image_bytes)

            # Determine filename
            filename = self._generate_filename(opportunity)
            file_path = output_dir / filename

            # Save image
            await write_bytes_async(file_path, image_bytes)

            logger.info(f"Saved image to: {file_path}")

            return GeneratedImage(
                file_path=file_path,
                opportunity=opportunity,
                theme_profile=theme,
                generation_prompt=prompt,
                cost=self.IMAGEN_COST_PER_IMAGE,
            )

        except Exception as e:
            raise ImageGenerationError(
                f"Failed to generate image for {opportunity.semantic_context}: {e}"
            ) from e

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
            "icon": "-icon",
            "logo": "-logo",
            "button": "-button",
            "background": "-bg",
            "illustration": "-illust",
            "hero": "-hero",
        }
        suffix = suffix_map.get(opportunity.purpose.value, "")

        return f"{base}{suffix}.png"
