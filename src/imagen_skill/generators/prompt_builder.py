"""Prompt builder for generating Imagen prompts from context and theme."""

import logging

from ..core.models import ImagePurpose, Opportunity, ThemeProfile

logger = logging.getLogger("imagen_skill.prompt_builder")


class PromptBuilder:
    """Build Imagen prompts from opportunity context and theme."""

    # Purpose-specific prompt templates
    PURPOSE_TEMPLATES = {
        ImagePurpose.ICON: "{description} icon",
        ImagePurpose.LOGO: "{description} logo design",
        ImagePurpose.BUTTON: "{description} button graphic",
        ImagePurpose.BACKGROUND: "{description} background pattern",
        ImagePurpose.ILLUSTRATION: "{description} illustration",
        ImagePurpose.HERO: "{description} hero image",
    }

    def build_prompt(self, opportunity: Opportunity, theme: ThemeProfile) -> str:
        """Build Imagen prompt from opportunity context and theme.

        Args:
            opportunity: Opportunity with semantic context and purpose
            theme: Theme profile with colors and style

        Returns:
            Optimized prompt for Imagen 3
        """
        # Base description from semantic context
        description = opportunity.semantic_context

        # Apply purpose-specific template
        base = self.PURPOSE_TEMPLATES.get(opportunity.purpose, "{description}").format(
            description=description
        )

        # Extract theme elements
        style = theme.style.aesthetic
        primary_color = theme.colors.primary
        keywords = ", ".join(theme.style.keywords[:3])  # Top 3 keywords

        # Build full prompt
        prompt_parts = [
            base,
            f"{style} style",
            f"using {primary_color} as primary color",
        ]

        if keywords:
            prompt_parts.append(keywords)

        # Add quality directive
        prompt_parts.append("high quality, professional design")

        # Add background requirement for icons/logos (for easy removal)
        if opportunity.purpose in [ImagePurpose.ICON, ImagePurpose.LOGO]:
            prompt_parts.append("on solid white background for easy removal")

        # Add size hint if available
        if opportunity.size_hint:
            prompt_parts.append(f"{opportunity.size_hint} resolution")

        prompt = ", ".join(prompt_parts)

        logger.debug(f"Built prompt for {opportunity.purpose}: {prompt}")

        return prompt

    def determine_aspect_ratio(self, opportunity: Opportunity) -> str:
        """Determine appropriate aspect ratio for opportunity.

        Args:
            opportunity: Opportunity with purpose and size hints

        Returns:
            Aspect ratio string (1:1, 16:9, etc.)
        """
        # Parse size hint if available
        if opportunity.size_hint:
            try:
                parts = opportunity.size_hint.lower().replace("x", " ").split()
                if len(parts) == 2:
                    width, height = int(parts[0]), int(parts[1])
                    ratio = width / height

                    if 0.9 <= ratio <= 1.1:
                        return "1:1"
                    elif ratio > 1.5:
                        return "16:9"
                    elif ratio < 0.7:
                        return "9:16"
            except (ValueError, ZeroDivisionError):
                pass

        # Default aspect ratios by purpose
        purpose_ratios = {
            ImagePurpose.ICON: "1:1",
            ImagePurpose.LOGO: "4:3",
            ImagePurpose.BUTTON: "3:4",
            ImagePurpose.BACKGROUND: "16:9",
            ImagePurpose.ILLUSTRATION: "4:3",
            ImagePurpose.HERO: "16:9",
        }

        return purpose_ratios.get(opportunity.purpose, "1:1")
