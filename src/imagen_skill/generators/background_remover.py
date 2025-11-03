"""Background removal using rembg library."""

import asyncio
import logging
from io import BytesIO

from PIL import Image
from rembg import new_session, remove

from ..exceptions import BackgroundRemovalError

logger = logging.getLogger("imagen_skill.background_remover")


class BackgroundRemover:
    """Remove backgrounds from images using rembg."""

    def __init__(self, model_name: str = "u2net"):
        """Initialize background remover.

        Args:
            model_name: rembg model to use (u2net, u2netp, birefnet-general, etc.)
        """
        self.model_name = model_name
        self.session = None

    def _ensure_session(self) -> None:
        """Ensure rembg session is initialized."""
        if self.session is None:
            logger.info(f"Initializing rembg session with model: {self.model_name}")
            self.session = new_session(self.model_name)

    async def remove(self, image_bytes: bytes) -> bytes:
        """Remove background from image.

        Args:
            image_bytes: Input image as bytes

        Returns:
            Output image with transparent background as bytes (PNG)

        Raises:
            BackgroundRemovalError: If removal fails
        """
        try:
            self._ensure_session()

            # Run in executor since rembg is synchronous
            loop = asyncio.get_event_loop()
            output_bytes = await loop.run_in_executor(None, self._remove_sync, image_bytes)

            logger.info(f"Background removed: {len(image_bytes)} -> {len(output_bytes)} bytes")

            return output_bytes

        except Exception as e:
            raise BackgroundRemovalError(f"Background removal failed: {e}") from e

    def _remove_sync(self, image_bytes: bytes) -> bytes:
        """Synchronous background removal (runs in executor).

        Args:
            image_bytes: Input image bytes

        Returns:
            Output image bytes with transparent background
        """
        # Convert bytes to PIL Image
        input_image = Image.open(BytesIO(image_bytes))

        # Remove background
        output_image = remove(input_image, session=self.session)

        # Convert back to bytes (PNG format to preserve transparency)
        output_buffer = BytesIO()
        output_image.save(output_buffer, format="PNG")

        return output_buffer.getvalue()
