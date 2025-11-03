"""CLI entry point for Imagen skill."""

import argparse
import asyncio
import sys
from pathlib import Path

from .core.config import Config
from .core.skill import ImagenSkill
from .exceptions import ImagenSkillError


def main() -> int:
    """Main CLI entry point.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description="Imagen UI Enhancement Skill - Generate and integrate themed images"
    )

    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="Code files to analyze",
    )

    parser.add_argument(
        "--theme",
        "-t",
        type=Path,
        help="Path to theme reference image",
    )

    parser.add_argument(
        "--project-root",
        "-p",
        type=Path,
        default=Path.cwd(),
        help="Project root directory (default: current directory)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate images and show diffs without applying changes",
    )

    parser.add_argument(
        "--max-images",
        "-m",
        type=int,
        help="Maximum number of images to generate",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    # Validate files exist
    for file_path in args.files:
        if not file_path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            return 1

    # Validate theme reference if provided
    if args.theme and not args.theme.exists():
        print(f"Error: Theme reference not found: {args.theme}", file=sys.stderr)
        return 1

    try:
        # Load configuration
        config = Config()
        if args.debug:
            config.debug = True

        # Create and execute skill
        skill = ImagenSkill(config)

        result = asyncio.run(
            skill.execute(
                target_files=args.files,
                theme_reference=args.theme,
                project_root=args.project_root,
                dry_run=args.dry_run,
                max_images=args.max_images,
            )
        )

        # Print summary
        print()
        print("=" * 60)
        print("UI Enhancement Complete")
        print("=" * 60)
        print(f"Opportunities found:     {result.opportunities_found}")
        print(f"Images generated:        {result.images_generated}")
        print(f"Integrations completed:  {result.integrations_completed}")
        print(f"Files modified:          {len(result.files_modified)}")
        print(f"Total cost:              ${result.total_cost:.2f}")
        print(f"Processing time:         {result.processing_time_seconds:.1f}s")

        if result.files_modified:
            print()
            print("Modified files:")
            for file_path in result.files_modified:
                print(f"  - {file_path}")

        if result.errors:
            print()
            print(f"Errors ({len(result.errors)}):")
            for error in result.errors:
                print(f"  - {error}")

        print("=" * 60)

        return 0 if result.success else 1

    except ImagenSkillError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if args.debug:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
