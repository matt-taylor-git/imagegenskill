"""Main skill orchestrator for Imagen UI Enhancement."""

import logging
import time
from pathlib import Path

from ..analyzers.code_analyzer import CodeAnalyzer
from ..analyzers.theme_analyzer import ThemeAnalyzer
from ..core.config import Config
from ..core.models import SkillResult, ThemeProfile
from ..exceptions import ImagenSkillError
from ..generators.background_remover import BackgroundRemover
from ..generators.image_generator import ImageGenerator
from ..generators.prompt_builder import PromptBuilder
from ..integrators.asset_manager import AssetManager
from ..integrators.code_integrator import CodeIntegrator
from ..services.gemini_client import GeminiClient
from ..utils.logging import setup_logging

logger = logging.getLogger("imagen_skill.skill")


class ImagenSkill:
    """Main orchestrator for autonomous UI enhancement."""

    def __init__(self, config: Config):
        """Initialize skill with configuration.

        Args:
            config: Application configuration
        """
        self.config = config

        # Setup logging
        setup_logging(config.log_level, config.debug)

        # Initialize components
        self.gemini_client = GeminiClient(config)
        self.theme_analyzer = ThemeAnalyzer(self.gemini_client)
        self.code_analyzer = CodeAnalyzer()
        self.prompt_builder = PromptBuilder()
        self.background_remover = BackgroundRemover(config.rembg_model)
        self.image_generator = ImageGenerator(
            self.gemini_client,
            self.prompt_builder,
            self.background_remover,
        )
        self.asset_manager = AssetManager()
        self.code_integrator = CodeIntegrator()

    async def execute(
        self,
        target_files: list[Path],
        theme_reference: Path | None = None,
        project_root: Path | None = None,
        dry_run: bool = False,
        max_images: int | None = None,
    ) -> SkillResult:
        """Execute skill: analyze, generate, integrate.

        Args:
            target_files: Code files to analyze
            theme_reference: Path to theme reference image
            project_root: Project root directory (defaults to current dir)
            dry_run: If True, don't apply changes
            max_images: Maximum number of images to generate (None = unlimited)

        Returns:
            SkillResult with execution summary

        Raises:
            ImagenSkillError: If execution fails
        """
        start_time = time.time()
        errors: list[str] = []
        files_modified: list[Path] = []
        total_cost = 0.0

        if project_root is None:
            project_root = Path.cwd()

        logger.info("=" * 60)
        logger.info("Imagen UI Enhancement Skill - Starting")
        logger.info("=" * 60)

        try:
            # Phase 1: Analyze theme
            theme: ThemeProfile | None = None
            if theme_reference and theme_reference.exists():
                logger.info(f"Phase 1: Analyzing theme from {theme_reference.name}")
                theme = await self.theme_analyzer.analyze(theme_reference)
                logger.info(f"  Theme: {theme.style.aesthetic}, Primary: {theme.colors.primary}")
            else:
                logger.warning("No theme reference provided, using defaults")
                # Create default theme
                from ..core.models import ColorPalette, VisualStyle

                theme = ThemeProfile(
                    colors=ColorPalette(
                        primary="#3B82F6",
                        secondary=["#10B981", "#8B5CF6"],
                        accent=["#F59E0B"],
                        background="#FFFFFF",
                        text="#1F2937",
                    ),
                    style=VisualStyle(
                        aesthetic="modern minimal",
                        mood="professional",
                        keywords=["clean", "simple", "rounded"],
                    ),
                    patterns=[],
                )

            # Phase 2: Analyze code
            logger.info(f"Phase 2: Analyzing {len(target_files)} code file(s)")
            opportunities = await self.code_analyzer.analyze(target_files, project_root)
            logger.info(f"  Found {len(opportunities)} opportunities")

            if not opportunities:
                logger.warning("No opportunities found")
                return SkillResult(
                    success=True,
                    theme=theme,
                    opportunities_found=0,
                    images_generated=0,
                    integrations_completed=0,
                    total_cost=0.0,
                    processing_time_seconds=time.time() - start_time,
                )

            # Limit opportunities if max_images specified
            if max_images:
                opportunities = opportunities[:max_images]
                logger.info(f"  Limited to {len(opportunities)} opportunities")

            # Phase 3: Generate images
            logger.info(f"Phase 3: Generating {len(opportunities)} image(s)")
            generated_images = []

            for i, opportunity in enumerate(opportunities, 1):
                try:
                    logger.info(
                        f"  [{i}/{len(opportunities)}] Generating {opportunity.purpose.value} "
                        f"for '{opportunity.semantic_context}'"
                    )

                    # Determine save location
                    save_path = self.asset_manager.determine_save_path(opportunity, project_root)
                    output_dir = save_path.parent

                    # Generate image
                    generated_image = await self.image_generator.generate(
                        opportunity, theme, output_dir
                    )
                    generated_images.append(generated_image)
                    total_cost += generated_image.cost

                    # Check cost limit
                    if total_cost >= self.config.max_cost_per_session:
                        logger.warning(
                            f"Cost limit reached: ${total_cost:.2f} >= ${self.config.max_cost_per_session:.2f}"
                        )
                        break

                except Exception as e:
                    error_msg = f"Failed to generate image for {opportunity.semantic_context}: {e}"
                    logger.error(error_msg)
                    errors.append(error_msg)
                    continue

            logger.info(f"  Generated {len(generated_images)} image(s)")

            # Phase 4: Integrate into code
            logger.info(f"Phase 4: Integrating into code (dry_run={dry_run})")
            integrations_completed = 0

            for i, generated_image in enumerate(generated_images, 1):
                try:
                    logger.info(
                        f"  [{i}/{len(generated_images)}] Integrating {generated_image.file_path.name}"
                    )

                    result = await self.code_integrator.integrate(
                        generated_image, project_root, dry_run
                    )

                    if result.success:
                        integrations_completed += 1
                        if result.file_path not in files_modified:
                            files_modified.append(result.file_path)

                        if result.diff:
                            logger.debug(f"Diff:\n{result.diff}")
                    else:
                        errors.append(result.error or "Unknown integration error")

                except Exception as e:
                    error_msg = f"Failed to integrate {generated_image.file_path.name}: {e}"
                    logger.error(error_msg)
                    errors.append(error_msg)
                    continue

            # Summary
            processing_time = time.time() - start_time
            logger.info("=" * 60)
            logger.info("Execution Summary")
            logger.info("=" * 60)
            logger.info(f"  Opportunities found:      {len(opportunities)}")
            logger.info(f"  Images generated:         {len(generated_images)}")
            logger.info(f"  Integrations completed:   {integrations_completed}")
            logger.info(f"  Files modified:           {len(files_modified)}")
            logger.info(f"  Total cost:               ${total_cost:.2f}")
            logger.info(f"  Processing time:          {processing_time:.1f}s")
            if errors:
                logger.warning(f"  Errors:                   {len(errors)}")
            logger.info("=" * 60)

            return SkillResult(
                success=len(errors) == 0,
                theme=theme,
                opportunities_found=len(opportunities),
                images_generated=len(generated_images),
                integrations_completed=integrations_completed,
                total_cost=total_cost,
                processing_time_seconds=processing_time,
                files_modified=files_modified,
                errors=errors,
            )

        except Exception as e:
            error_msg = f"Skill execution failed: {e}"
            logger.error(error_msg)
            raise ImagenSkillError(error_msg) from e
