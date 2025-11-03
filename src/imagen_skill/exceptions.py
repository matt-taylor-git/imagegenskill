"""Custom exception classes for Imagen skill."""


class ImagenSkillError(Exception):
    """Base exception for all Imagen skill errors."""

    pass


class APIError(ImagenSkillError):
    """Exception raised for API-related errors (Gemini, Imagen)."""

    pass


class ValidationError(ImagenSkillError):
    """Exception raised for data validation errors."""

    pass


class IntegrationError(ImagenSkillError):
    """Exception raised for code integration errors."""

    pass


class ParsingError(ImagenSkillError):
    """Exception raised for code parsing errors."""

    pass


class ThemeAnalysisError(ImagenSkillError):
    """Exception raised for theme analysis errors."""

    pass


class ImageGenerationError(ImagenSkillError):
    """Exception raised for image generation errors."""

    pass


class BackgroundRemovalError(ImagenSkillError):
    """Exception raised for background removal errors."""

    pass


class FileOperationError(ImagenSkillError):
    """Exception raised for file operation errors."""

    pass


class ConfigurationError(ImagenSkillError):
    """Exception raised for configuration errors."""

    pass
