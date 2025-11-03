"""Async client for Google Gemini API (Vision and Imagen)."""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any

from google import genai
from google.genai.types import GenerateContentConfig, GenerateImagesConfig
from PIL import Image

from ..core.config import Config
from ..exceptions import APIError

logger = logging.getLogger("imagen_skill.gemini_client")


class GeminiClient:
    """Async client for Gemini API interactions."""

    def __init__(self, config: Config):
        """Initialize Gemini client.

        Args:
            config: Application configuration with API key
        """
        self.config = config
        self.api_key = config.google_api_key
        self.timeout = config.timeout
        self.max_retries = config.max_retries

        # Configure Gemini API
        self.client = genai.Client(api_key=self.api_key)

    async def analyze_image_vision(self, image_path: Path, prompt: str) -> dict[str, Any]:
        """Analyze image using Gemini Vision with structured JSON output.

        Args:
            image_path: Path to image file
            prompt: Analysis prompt

        Returns:
            Parsed JSON response as dictionary

        Raises:
            APIError: If API call fails
        """
        try:
            # Load image
            image = Image.open(image_path)

            # Configure for JSON response
            config = GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2,  # Lower temp for consistent extraction
            )

            # Run in executor since genai is synchronous
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.models.generate_content(
                    model=self.config.vision_model,
                    contents=[prompt, image],
                    config=config,
                ),
            )

            # Parse JSON response
            result = json.loads(response.text)
            logger.debug(f"Vision analysis result: {result}")
            return result

        except json.JSONDecodeError as e:
            raise APIError(f"Failed to parse Vision API response as JSON: {e}") from e
        except Exception as e:
            raise APIError(f"Vision API call failed: {e}") from e

    async def generate_image(
        self,
        prompt: str,
        aspect_ratio: str = "1:1",
        number_of_images: int = 1,
    ) -> bytes:
        """Generate image using Imagen 3 API.

        Args:
            prompt: Image generation prompt
            aspect_ratio: Aspect ratio (1:1, 16:9, 9:16, 4:3, 3:4)
            number_of_images: Number of images to generate (1-4)

        Returns:
            Image bytes (PNG format)

        Raises:
            APIError: If generation fails
        """
        loop = asyncio.get_event_loop()

        for attempt in range(self.max_retries):
            try:
                # Configure generation
                generation_config = GenerateImagesConfig(
                    number_of_images=number_of_images,
                    aspect_ratio=aspect_ratio,
                    safety_filter_level="block_medium_and_above",
                )

                # Generate image (synchronous call wrapped in executor)
                response = await loop.run_in_executor(
                    None,
                    lambda cfg=generation_config: self.client.models.generate_images(
                        model=self.config.default_image_model,
                        prompt=prompt,
                        config=cfg,
                    ),
                )

                # Extract first generated image as bytes
                if not response.generated_images:
                    raise APIError("No images generated in response")

                generated_image = response.generated_images[0]

                # Convert PIL Image to bytes
                import io

                buffer = io.BytesIO()
                generated_image.image.save(buffer, format="PNG")
                image_bytes = buffer.getvalue()

                logger.info(f"Generated image: {len(image_bytes)} bytes")
                return image_bytes

            except Exception as e:
                error_msg = str(e)

                # Check for rate limiting
                if "429" in error_msg and attempt < self.max_retries - 1:
                    wait_time = 2**attempt
                    logger.warning(f"Rate limited, retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    continue

                raise APIError(f"Image generation failed: {e}") from e

        raise APIError(f"Image generation failed after {self.max_retries} retries")
