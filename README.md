# Imagen UI Enhancement Skill

An autonomous Claude Code skill that analyzes code, generates theme-consistent images using Gemini Imagen 3, and integrates them into codebases.

## Features

- **Theme Analysis**: Extract visual styles and color palettes from reference images using Gemini Vision
- **Code Analysis**: Automatically detect UI enhancement opportunities in Qt C++, React, Unity, and HTML code
- **Image Generation**: Create themed images using Gemini Imagen 3 API
- **Background Removal**: Automatically remove backgrounds from icons and logos
- **Code Integration**: Update source files with generated image references
- **Resource Management**: Handle Qt .qrc files and framework-specific asset structures

## Installation

### Requirements

- Python >= 3.10, < 3.14
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### Install

```bash
# Clone the repository
git clone <repository-url>
cd imagegenskill

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package with dependencies
pip install -e ".[dev]"
```

### Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Google API key:
```bash
GOOGLE_API_KEY=your-google-api-key-here
```

## Usage

### Basic Usage

```bash
# Analyze a Qt C++ file with a theme reference
imagen-skill path/to/mainwindow.cpp --theme path/to/theme-screenshot.png

# Analyze multiple files
imagen-skill src/*.cpp --theme theme.png --project-root .

# Dry run (generate images but don't modify code)
imagen-skill mainwindow.cpp --theme theme.png --dry-run

# Limit number of images generated
imagen-skill mainwindow.cpp --theme theme.png --max-images 3
```

### Command Line Options

```
usage: imagen-skill [-h] [--theme THEME] [--project-root PROJECT_ROOT]
                    [--dry-run] [--max-images MAX_IMAGES] [--debug]
                    files [files ...]

positional arguments:
  files                   Code files to analyze

options:
  -h, --help              Show this help message
  --theme, -t THEME       Path to theme reference image
  --project-root, -p DIR  Project root directory (default: current dir)
  --dry-run               Generate images without applying changes
  --max-images, -m N      Maximum number of images to generate
  --debug                 Enable debug logging
```

## Supported Frameworks

### Qt C++ (Phase 1 - Implemented)

Detects:
- `button.setIcon(QIcon())` - Empty icon assignments
- `QIcon("")` - Empty icon constructors
- `setWindowIcon(QIcon())` - Window icon assignments
- `QPixmap varname;` - Uninitialized pixmap declarations
- `QPixmap("placeholder.png")` - Placeholder images

Automatically updates `.qrc` resource files.

### Future Support

- React/JSX - Planned
- Unity C# - Planned
- HTML/CSS - Planned

## Architecture

```
src/imagen_skill/
├── core/
│   ├── config.py          # Pydantic configuration
│   ├── models.py          # Data models
│   └── skill.py           # Main orchestrator
├── analyzers/
│   ├── theme_analyzer.py  # Theme extraction
│   ├── code_analyzer.py   # Code analysis
│   └── parsers/           # Framework-specific parsers
├── generators/
│   ├── prompt_builder.py  # Prompt generation
│   ├── image_generator.py # Image generation
│   └── background_remover.py  # Background removal
├── integrators/
│   ├── code_integrator.py # Code modification
│   ├── asset_manager.py   # File management
│   └── frameworks/        # Framework-specific integrators
├── services/
│   └── gemini_client.py   # Gemini API client
└── utils/
    ├── logging.py         # Logging setup
    └── file_utils.py      # File operations
```

## Development

### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/imagen_skill --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_models.py -v
```

### Code Quality

```bash
# Format code
ruff format src/

# Lint
ruff check src/ --fix

# Type check
mypy src/imagen_skill/
```

## Cost Estimates

- Theme analysis: ~$0.01 per image
- Image generation: ~$0.03-0.04 per image
- Typical session (5 images): ~$0.15-0.20

Cost limits can be configured via `MAX_COST_PER_SESSION` environment variable.

## Troubleshooting

### "No opportunities found"

- Ensure your code files contain recognized patterns (e.g., `QIcon()` for Qt)
- Check that the framework is correctly detected (look for imports/includes)
- Use `--debug` flag for detailed analysis logs

### "API Error: 429"

- Rate limited by Gemini API
- The skill automatically retries with exponential backoff
- Consider reducing `--max-images` or adding delays between runs

### "Background removal failed"

- Ensure rembg model is downloaded (happens automatically on first run)
- Check that you have sufficient disk space (~170MB for u2net model)
- Try a different model via `REMBG_MODEL` environment variable

## License

MIT

## Contributing

Contributions welcome! Please read the PRP documentation in `PRPs/` for implementation patterns.
