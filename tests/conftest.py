"""Shared pytest fixtures for Imagen skill tests."""

from unittest.mock import AsyncMock

import pytest

from imagen_skill.core.config import Config
from imagen_skill.core.models import (
    ColorPalette,
    ThemeProfile,
    VisualStyle,
)


@pytest.fixture
def mock_config() -> Config:
    """Create mock configuration for testing."""
    return Config(
        google_api_key="test-api-key",
        timeout=120,
        max_retries=3,
        log_level="INFO",
        debug=False,
        max_cost_per_session=0.50,
    )


@pytest.fixture
def sample_theme() -> ThemeProfile:
    """Create sample theme profile for testing."""
    return ThemeProfile(
        colors=ColorPalette(
            primary="#7C3AED",
            secondary=["#EC4899", "#F59E0B"],
            accent=["#10B981"],
            background="#1F2937",
            text="#F9FAFB",
        ),
        style=VisualStyle(
            aesthetic="modern minimal",
            mood="professional",
            keywords=["clean", "rounded", "shadow"],
            icon_style="outline",
        ),
        patterns=["rounded corners", "drop shadows"],
    )


@pytest.fixture
def sample_qt_code() -> str:
    """Sample Qt C++ code for testing."""
    return """
    #include <QApplication>
    #include <QPushButton>
    #include <QIcon>

    int main(int argc, char *argv[]) {
        QApplication app(argc, argv);

        QPushButton settingsButton("Settings");
        settingsButton.setIcon(QIcon());

        QPushButton profileButton("Profile");
        profileButton.setIcon(QIcon(""));

        return app.exec();
    }
    """


@pytest.fixture
def mock_gemini_client() -> AsyncMock:
    """Create mock Gemini client."""
    client = AsyncMock()
    client.analyze_image_vision = AsyncMock(
        return_value={
            "colors": {
                "primary": "#7C3AED",
                "secondary": ["#EC4899"],
                "accent": ["#10B981"],
                "background": "#FFFFFF",
                "text": "#000000",
            },
            "style": {
                "aesthetic": "modern minimal",
                "mood": "professional",
                "keywords": ["clean", "simple"],
                "icon_style": "outline",
            },
            "patterns": ["rounded corners"],
        }
    )
    client.generate_image = AsyncMock(return_value=b"fake-image-bytes")
    return client
