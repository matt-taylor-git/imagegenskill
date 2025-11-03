"""Async client for Google Gemini API (Vision and Imagen)."""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any

import google.generativeai as genai
from google import genai as genai_client
from google.genai import types
from google.generativeai.types import GenerationConfig
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

        # Configure Gemini API for vision
        genai.configure(api_key=self.api_key)

        # Initialize Gen AI client for Imagen
        self.imagen_client = genai_client.Client(api_key=self.api_key)

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
            config = GenerationConfig(
                response_mime_type="application/json",
                temperature=0.2,  # Lower temp for consistent extraction
            )

            # Run in executor since genai is synchronous
            loop = asyncio.get_event_loop()
            model = genai.GenerativeModel(self.config.vision_model)
            response = await loop.run_in_executor(
                None,
                lambda m=model, p=prompt, i=image, c=config: m.generate_content(
                    contents=[p, i],
                    generation_config=c,
                ),
            )

            # Parse JSON response
            result: dict[str, Any] = json.loads(response.text)
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
                generation_config = types.GenerateImagesConfig(
                    number_of_images=number_of_images,
                    aspect_ratio=aspect_ratio,
                )

                # Generate image (synchronous call wrapped in executor)
                response = await loop.run_in_executor(
                    None,
                    lambda cfg=generation_config, p=prompt: self.imagen_client.models.generate_images(
                        model=self.config.default_image_model,
                        prompt=p,
                        config=cfg,
                    ),
                )

                # Extract first generated image as bytes
                if not response.generated_images:
                    raise APIError("No images generated in response")

                generated_image = response.generated_images[0]

                # Extract bytes from the generated image
                image_bytes: bytes = generated_image.image.image_bytes

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
