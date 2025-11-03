"""Configuration management using Pydantic Settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Google Gemini API Configuration
    google_api_key: str = Field(
        ...,
        description="Google Gemini API key for Vision and Imagen access",
    )

    # API Settings
    timeout: int = Field(
        default=120,
        description="API request timeout in seconds",
        ge=1,
        le=600,
    )

    max_retries: int = Field(
        default=3,
        description="Maximum number of retry attempts for API calls",
        ge=0,
        le=10,
    )

    # Logging Configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )

    debug: bool = Field(
        default=False,
        description="Enable debug mode with verbose output",
    )

    # Imagen Generation Defaults
    default_aspect_ratio: str = Field(
        default="1:1",
        description="Default aspect ratio for image generation",
    )

    default_image_model: str = Field(
        default="imagen-3.0-generate-002",
        description="Default Imagen model to use",
    )

    # Cost Tracking
    max_cost_per_session: float = Field(
        default=0.50,
        description="Maximum API cost per skill execution session (USD)",
        ge=0.0,
    )

    # Theme Analysis
    vision_model: str = Field(
        default="gemini-2.0-flash-exp",
        description="Gemini model for vision/theme analysis",
    )

    # Background Removal
    rembg_model: str = Field(
        default="u2net",
        description="rembg model for background removal",
    )

    # File Operations
    default_output_format: str = Field(
        default="png",
        description="Default output format for generated images",
    )
