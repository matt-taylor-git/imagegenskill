"""Pydantic data models for type safety and validation."""

from datetime import datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


# Enums for type safety
class ImagePurpose(str, Enum):
    """Purpose/type of image to generate."""

    ICON = "icon"
    LOGO = "logo"
    BUTTON = "button"
    BACKGROUND = "background"
    ILLUSTRATION = "illustration"
    HERO = "hero"


class Framework(str, Enum):
    """UI framework/platform."""

    QT = "qt"
    REACT = "react"
    UNITY = "unity"
    HTML = "html"


class IntegrationType(str, Enum):
    """Type of code integration to perform."""

    QT_ICON = "qt_icon"
    QT_PIXMAP = "qt_pixmap"
    QT_RESOURCE = "qt_resource"
    REACT_IMPORT = "react_import"
    REACT_JSX = "react_jsx"
    HTML_IMG = "html_img"
    CSS_BACKGROUND = "css_background"
    UNITY_SPRITE = "unity_sprite"


# Theme Analysis Models
class ColorPalette(BaseModel):
    """Color palette extracted from theme."""

    primary: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    secondary: list[str] = Field(default_factory=list)
    accent: list[str] = Field(default_factory=list)
    background: str = Field(default="#FFFFFF")
    text: str = Field(default="#000000")


class VisualStyle(BaseModel):
    """Visual style characteristics."""

    aesthetic: str = Field(..., description="e.g., 'modern minimal', 'retro', 'playful'")
    mood: str = Field(default="professional")
    keywords: list[str] = Field(default_factory=list)
    icon_style: str | None = Field(default=None, description="e.g., 'outline', 'filled'")


class ThemeProfile(BaseModel):
    """Complete theme profile for image generation."""

    colors: ColorPalette
    style: VisualStyle
    patterns: list[str] = Field(default_factory=list)
    source_image: str | None = None


# Code Analysis Models
class CodeLocation(BaseModel):
    """Location in source code."""

    file_path: Path
    line_number: int = Field(..., ge=1)
    column: int | None = None


class Opportunity(BaseModel):
    """UI enhancement opportunity detected in code."""

    location: CodeLocation
    purpose: ImagePurpose
    semantic_context: str = Field(..., description="e.g., 'settings', 'profile'")
    code_snippet: str
    integration_type: IntegrationType
    confidence: float = Field(..., ge=0.0, le=1.0)
    size_hint: str | None = None  # e.g., "32x32", "128x128"
    framework: Framework


# Image Generation Models
class GenerationRequest(BaseModel):
    """Request for image generation."""

    prompt: str = Field(..., min_length=1, max_length=2000)
    aspect_ratio: str = Field(default="1:1", pattern=r"^(1:1|16:9|9:16|4:3|3:4)$")
    remove_background: bool = True

    @field_validator("aspect_ratio")
    @classmethod
    def validate_aspect_ratio(cls, v: str) -> str:
        """Validate aspect ratio format."""
        valid_ratios = ["1:1", "16:9", "9:16", "4:3", "3:4"]
        if v not in valid_ratios:
            raise ValueError(f"Aspect ratio must be one of {valid_ratios}")
        return v


class GeneratedImage(BaseModel):
    """Generated image with metadata."""

    file_path: Path
    opportunity: Opportunity
    theme_profile: ThemeProfile
    generation_prompt: str
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    cost: float = Field(default=0.0, ge=0.0)


# Integration Models
class IntegrationResult(BaseModel):
    """Result of code integration."""

    success: bool
    file_path: Path
    diff: str = Field(default="")
    error: str | None = None


# Skill Execution Result
class SkillResult(BaseModel):
    """Final result of skill execution."""

    success: bool
    theme: ThemeProfile | None = None
    opportunities_found: int = Field(default=0, ge=0)
    images_generated: int = Field(default=0, ge=0)
    integrations_completed: int = Field(default=0, ge=0)
    total_cost: float = Field(default=0.0, ge=0.0)
    processing_time_seconds: float = Field(default=0.0, ge=0.0)
    files_modified: list[Path] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
