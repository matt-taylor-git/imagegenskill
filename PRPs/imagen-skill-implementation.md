name: "Imagen UI Enhancement Skill - Implementation PRP"
description: |
  Complete implementation guide for building an autonomous Claude Code skill that analyzes code,
  generates themed images using Gemini Imagen 3, and integrates them into codebases.

---

## Goal

**Feature Goal**: Build a fully autonomous Claude Code skill that can analyze source code files (Qt C++, React, Unity, HTML), identify UI enhancement opportunities, generate theme-consistent images using Gemini Imagen 3 API, remove backgrounds, and automatically integrate the generated assets into the codebase.

**Deliverable**: A production-ready Python skill package that:
- Accepts theme references and target code files
- Autonomously identifies where images would improve UI
- Generates images matching the provided theme
- Integrates generated assets with proper code updates
- Reports progress and costs to the user

**Success Definition**:
- Skill successfully completes end-to-end workflow (analysis → generation → integration)
- 85%+ of identified opportunities are appropriate and accepted by users
- 95%+ of code integrations compile without errors
- All validation gates pass (lint, type check, tests)
- Complete documentation and example usage

## User Persona

**Target User**: Software developers building UI-heavy applications (desktop apps, web apps, games)

**Use Case**: Developer wants to quickly polish UI by adding professionally-designed, theme-consistent images without leaving their workflow or using design tools.

**User Journey**:
1. Developer invokes Claude Code with theme reference and target file(s)
2. Claude Code recognizes the request and invokes Imagen skill
3. Skill autonomously analyzes theme, identifies opportunities, generates images
4. Skill integrates images into code and resource files
5. Developer reviews changes and iterates if needed

**Pain Points Addressed**:
- Manual image creation is time-consuming (30-60 min per component)
- Context switching between code, design tools, and asset management
- Inconsistent theming across manually created assets
- Manual integration of assets into code after creation

## Why

- **Developer Productivity**: Reduce UI polish time from hours to minutes (20x faster)
- **Theme Consistency**: Automated theme extraction ensures visual coherence
- **Autonomous Operation**: Works without manual intervention once invoked
- **Multi-Framework Support**: Works with Qt, React, Unity, HTML (Phase 1 focuses on Qt)
- **Integration with Claude Code**: Leverages existing skill invocation system

## What

The skill will:
1. **Analyze theme images** using Gemini Vision to extract colors, styles, patterns
2. **Parse code files** to identify UI enhancement opportunities (empty icons, placeholders, etc.)
3. **Generate theme-consistent images** using Gemini Imagen 3 API
4. **Remove backgrounds** from icons/logos using rembg library
5. **Integrate assets** by updating code and resource files automatically
6. **Track metadata** for all generated images and integrations
7. **Report results** with detailed breakdown of changes, costs, and next steps

### Success Criteria

- [ ] Theme analyzer extracts color palettes and style keywords from reference images
- [ ] Code analyzer detects 3+ opportunity types in Qt C++ code (icons, logos, backgrounds)
- [ ] Image generator produces images matching theme with 90%+ user satisfaction
- [ ] Background remover creates clean transparent PNGs for icons/logos
- [ ] Code integrator updates files without breaking syntax (95%+ success rate)
- [ ] All validation gates pass: mypy, ruff, pytest (100% pass rate)
- [ ] End-to-end workflow completes in <60 seconds for 5 images
- [ ] Cost per session stays under $0.50 for typical usage
- [ ] Comprehensive test coverage (80%+ code coverage)

## All Needed Context

### Context Completeness Check

_This PRP provides: PRD requirements, Python project structure patterns, API integration guidance, code parsing strategies, validation approach, and complete file-by-file implementation tasks. An AI agent with no prior knowledge of this codebase should be able to implement successfully using this PRP and the referenced documentation._

### Documentation & References

```yaml
# MUST READ - External Documentation

- url: https://ai.google.dev/gemini-api/docs/vision
  why: Gemini Vision API for analyzing theme images and extracting visual properties
  critical: Use structured output with JSON schema for consistent theme extraction
  section: "Multimodal prompts with images"

- url: https://ai.google.dev/gemini-api/docs/imagen
  why: Imagen 3 API for generating images from text prompts
  critical: Use aspect_ratio parameter (1:1, 16:9) and safety settings
  section: "Generate images" and "API reference"

- url: https://github.com/danielgatis/rembg
  why: rembg library for removing backgrounds from generated images
  critical: Use u2net model for best quality, handle PIL Image objects
  section: README examples

- url: https://docs.pydantic.dev/latest/
  why: Pydantic v2 for data validation and settings management
  critical: Use BaseModel for all API requests/responses, BaseSettings for config
  section: "Models" and "Settings management"

- url: https://docs.pytest.org/en/stable/how-to/asyncio.html
  why: pytest-asyncio for testing async functions
  critical: Use @pytest.mark.asyncio decorator and asyncio_mode = "auto"
  section: "How to test asyncio code"

# MUST CREATE - Project Documentation

- docfile: PRPs/ai_docs/gemini_api_patterns.md
  why: Custom patterns for Gemini API authentication, error handling, rate limiting
  section: All sections - create comprehensive guide

- docfile: PRPs/ai_docs/code_parsing_patterns.md
  why: Patterns for parsing Qt C++, React, Unity code to find image opportunities
  section: All sections - include regex patterns and heuristics

- docfile: PRPs/ai_docs/qt_resource_system.md
  why: Qt .qrc resource file format and integration patterns
  section: How to add resources and reference them in C++ code
```

### Current Codebase Tree

```bash
# Current state (minimal starter project)
imagegenskill/
├── .claude/
│   └── commands/           # Slash command definitions (if any)
├── .git/
├── PRPs/
│   ├── ai_docs/           # Documentation for AI context (to be populated)
│   ├── README.md          # PRP concept explanation
│   ├── imagen-skill-prd-v2.md  # Complete PRD (MUST READ)
│   ├── prp_base.md        # Template used for this PRP
│   └── [other templates]
└── (empty - no src/ yet)
```

### Desired Codebase Tree with Files to be Added

```bash
imagegenskill/
├── src/
│   └── imagen_skill/
│       ├── __init__.py                    # Package initialization, version
│       ├── main.py                        # Skill entry point, CLI interface
│       ├── core/
│       │   ├── __init__.py
│       │   ├── skill.py                   # ImagenSkill main orchestrator class
│       │   ├── models.py                  # Pydantic models (requests, responses, theme profiles)
│       │   └── config.py                  # Configuration management with env vars
│       ├── analyzers/
│       │   ├── __init__.py
│       │   ├── theme_analyzer.py          # ThemeAnalyzer - extracts theme from reference image
│       │   ├── code_analyzer.py           # CodeAnalyzer - finds opportunities in code
│       │   └── parsers/
│       │       ├── __init__.py
│       │       ├── base.py                # BaseParser abstract class
│       │       ├── qt_parser.py           # QtCodeParser - parses Qt C++ code
│       │       ├── react_parser.py        # ReactCodeParser (future)
│       │       └── patterns.py            # Regex patterns and heuristics
│       ├── generators/
│       │   ├── __init__.py
│       │   ├── image_generator.py         # ImageGenerator - calls Imagen API
│       │   ├── prompt_builder.py          # PromptBuilder - creates prompts from context + theme
│       │   └── background_remover.py      # BackgroundRemover - uses rembg
│       ├── integrators/
│       │   ├── __init__.py
│       │   ├── code_integrator.py         # CodeIntegrator - updates code files
│       │   ├── asset_manager.py           # AssetManager - manages file placement
│       │   └── frameworks/
│       │       ├── __init__.py
│       │       ├── base.py                # BaseIntegrator abstract class
│       │       ├── qt_integrator.py       # QtIntegrator - updates Qt code and .qrc
│       │       └── react_integrator.py    # ReactIntegrator (future)
│       ├── services/
│       │   ├── __init__.py
│       │   ├── gemini_client.py           # GeminiClient - async API client for Gemini
│       │   └── cache.py                   # Cache - optional caching layer
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── logging.py                 # Structured logging setup
│       │   ├── file_utils.py              # File operations utilities
│       │   └── validators.py              # Input validation helpers
│       ├── exceptions.py                  # Custom exception classes
│       └── types.py                       # Type definitions, enums, protocols
├── tests/
│   ├── __init__.py
│   ├── conftest.py                        # Shared pytest fixtures
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_theme_analyzer.py
│   │   ├── test_code_analyzer.py
│   │   ├── test_prompt_builder.py
│   │   └── test_qt_parser.py
│   ├── integration/
│   │   ├── test_gemini_client.py
│   │   ├── test_image_generation_flow.py
│   │   └── test_end_to_end.py
│   └── fixtures/
│       ├── sample_code/
│       │   ├── mainwindow.cpp             # Sample Qt code for testing
│       │   └── resources.qrc
│       ├── sample_images/
│       │   └── theme_reference.png
│       └── mock_responses.py              # Mock API responses
├── docs/
│   ├── architecture.md
│   ├── api_reference.md
│   └── development.md
├── PRPs/
│   └── ai_docs/
│       ├── gemini_api_patterns.md         # To be created
│       ├── code_parsing_patterns.md       # To be created
│       └── qt_resource_system.md          # To be created
├── .env.example                           # Example environment variables
├── .gitignore
├── pyproject.toml                         # Python project configuration
├── README.md
└── LICENSE
```

### Known Gotchas & Library Quirks

```python
# CRITICAL: Gemini API Authentication
# - Requires GOOGLE_API_KEY environment variable
# - Use google-generativeai library (pip install google-generativeai)
# - Initialize with: genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# CRITICAL: Gemini Vision for Theme Analysis
# - Can accept PIL Image objects or file paths
# - Use structured output with response_mime_type="application/json" for JSON responses
# - Example: model.generate_content([prompt, image], generation_config={"response_mime_type": "application/json"})

# CRITICAL: Imagen 3 API
# - Model name: "imagen-3.0-generate-001" or "imagen-3.0-generate-002"
# - Aspect ratios: "1:1", "16:9", "9:16", "4:3", "3:4"
# - Returns image as bytes, need to decode and save
# - Cost: ~$0.03-0.04 per image generation

# CRITICAL: rembg Library
# - Works with PIL Image objects
# - Model loading can be slow first time (downloads ~170MB u2net model)
# - Usage: output = remove(input_image)  # Returns PIL Image with transparent background
# - Handle as: from rembg import remove; output = remove(Image.open("input.png"))

# CRITICAL: Qt Resource Files (.qrc)
# - XML format with <RCC><qresource> structure
# - Resources referenced in C++ with ":/" prefix (e.g., ":/resources/icons/settings.png")
# - Must be compiled with rcc or handled by build system
# - Update .qrc file whenever adding new resources

# CRITICAL: Async/Await Patterns
# - All API calls should be async for better performance
# - Use httpx.AsyncClient for HTTP requests (not requests library)
# - Use aiofiles for async file I/O
# - Pytest requires @pytest.mark.asyncio for async tests

# CRITICAL: Pydantic V2 Validation
# - Use BaseModel for data models, BaseSettings for configuration
# - Field validation with Field(..., min_length=1, max_length=1000)
# - Custom validators with @field_validator decorator
# - Settings load from .env automatically with Config.model_config

# CRITICAL: Error Handling
# - Gemini API may rate limit (429 errors) - implement exponential backoff
# - Imagen generation may fail (safety filters) - handle gracefully and report to user
# - File write operations may fail (permissions) - validate paths before writing
# - Code parsing may encounter unexpected syntax - use try/except and skip gracefully
```

## Implementation Blueprint

### Data Models and Structure

Create comprehensive Pydantic models for type safety and validation across all components.

```python
# src/imagen_skill/core/models.py
from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import Optional, List, Dict, Literal
from enum import Enum
from pathlib import Path

# Enums for type safety
class ImagePurpose(str, Enum):
    ICON = "icon"
    LOGO = "logo"
    BUTTON = "button"
    BACKGROUND = "background"
    ILLUSTRATION = "illustration"
    HERO = "hero"

class Framework(str, Enum):
    QT = "qt"
    REACT = "react"
    UNITY = "unity"
    HTML = "html"

class IntegrationType(str, Enum):
    QT_ICON = "qt_icon"
    QT_PIXMAP = "qt_pixmap"
    QT_RESOURCE = "qt_resource"

# Theme Analysis Models
class ColorPalette(BaseModel):
    primary: str = Field(..., pattern="^#[0-9A-Fa-f]{6}$")
    secondary: List[str]
    accent: List[str]
    background: str
    text: str

class VisualStyle(BaseModel):
    aesthetic: str  # "modern minimal", "retro", etc.
    mood: str
    keywords: List[str]
    icon_style: Optional[str] = None

class ThemeProfile(BaseModel):
    colors: ColorPalette
    style: VisualStyle
    patterns: List[str]
    source_image: Optional[str] = None

# Opportunity Detection Models
class CodeLocation(BaseModel):
    file_path: Path
    line_number: int
    column: Optional[int] = None

class Opportunity(BaseModel):
    location: CodeLocation
    purpose: ImagePurpose
    semantic_context: str  # e.g., "settings", "profile"
    code_snippet: str
    integration_type: IntegrationType
    confidence: float = Field(..., ge=0.0, le=1.0)
    size_hint: Optional[str] = None  # e.g., "32x32"
    framework: Framework

# Image Generation Models
class GenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000)
    aspect_ratio: str = Field(default="1:1", pattern="^(1:1|16:9|9:16|4:3|3:4)$")
    remove_background: bool = True

class GeneratedImage(BaseModel):
    file_path: Path
    opportunity: Opportunity
    theme_profile: ThemeProfile
    generation_prompt: str
    created_at: str
    cost: float

# Integration Models
class IntegrationResult(BaseModel):
    success: bool
    file_path: Path
    diff: str
    error: Optional[str] = None

# Final Skill Result
class SkillResult(BaseModel):
    success: bool
    theme: ThemeProfile
    opportunities_found: int
    images_generated: int
    integrations_completed: int
    total_cost: float
    processing_time_seconds: float
    files_modified: List[Path]
    errors: List[str] = []
```

### Implementation Tasks (Ordered by Dependencies)

```yaml
# PHASE 1: FOUNDATION & SETUP

Task 1: CREATE pyproject.toml
  - IMPLEMENT: Complete Python project configuration with dependencies
  - INCLUDE: google-generativeai, rembg, pydantic>=2.0, httpx, aiofiles, pytest, mypy, ruff
  - NAMING: Follow modern pyproject.toml standard
  - PLACEMENT: Root directory
  - VALIDATION: uv pip install -e ".[dev]" succeeds

Task 2: CREATE src/imagen_skill/__init__.py
  - IMPLEMENT: Package initialization with version export
  - EXPORT: __version__ = "0.1.0"
  - PLACEMENT: src/imagen_skill/

Task 3: CREATE src/imagen_skill/core/config.py
  - IMPLEMENT: Config class using Pydantic BaseSettings
  - FIELDS: google_api_key, timeout, max_retries, log_level, debug
  - FOLLOW pattern: Load from .env using pydantic-settings
  - PLACEMENT: src/imagen_skill/core/

Task 4: CREATE src/imagen_skill/core/models.py
  - IMPLEMENT: All Pydantic models from Blueprint above
  - INCLUDE: Enums, validation, field constraints
  - PLACEMENT: src/imagen_skill/core/
  - VALIDATION: mypy passes, no type errors

Task 5: CREATE src/imagen_skill/exceptions.py
  - IMPLEMENT: Custom exception classes
  - CLASSES: ImagenSkillError, APIError, ValidationError, IntegrationError, ParsingError
  - PLACEMENT: src/imagen_skill/

Task 6: CREATE src/imagen_skill/types.py
  - IMPLEMENT: Type aliases and Protocol definitions
  - PLACEMENT: src/imagen_skill/

Task 7: CREATE src/imagen_skill/utils/logging.py
  - IMPLEMENT: Structured logging configuration
  - USE: structlog or standard logging with JSON formatter
  - PLACEMENT: src/imagen_skill/utils/

# PHASE 2: EXTERNAL API INTEGRATION

Task 8: CREATE src/imagen_skill/services/gemini_client.py
  - IMPLEMENT: GeminiClient async class for Gemini API interaction
  - METHODS: async def analyze_image_vision(), async def generate_image()
  - FOLLOW pattern: Use google-generativeai library with async/await
  - ERROR HANDLING: Retry logic with exponential backoff for 429 errors
  - DEPENDENCIES: Requires Task 3 (Config), Task 4 (Models)
  - PLACEMENT: src/imagen_skill/services/
  - VALIDATION: Mock API responses in tests

Task 9: CREATE tests/unit/test_gemini_client.py
  - IMPLEMENT: Unit tests for GeminiClient with mocked API
  - MOCK: google.generativeai responses using unittest.mock.AsyncMock
  - TEST CASES: Successful generation, rate limiting, error handling
  - PLACEMENT: tests/unit/

# PHASE 3: THEME ANALYSIS

Task 10: CREATE src/imagen_skill/analyzers/theme_analyzer.py
  - IMPLEMENT: ThemeAnalyzer class with async def analyze(image_path) -> ThemeProfile
  - USE: GeminiClient for vision API calls with structured JSON output
  - PROMPT: Extract color palette, visual style, design patterns
  - DEPENDENCIES: Task 8 (GeminiClient), Task 4 (Models)
  - PLACEMENT: src/imagen_skill/analyzers/
  - VALIDATION: Test with sample theme image

Task 11: CREATE tests/unit/test_theme_analyzer.py
  - IMPLEMENT: Unit tests for ThemeAnalyzer
  - MOCK: GeminiClient responses with sample theme data
  - TEST CASES: Valid theme extraction, missing colors, invalid responses
  - PLACEMENT: tests/unit/

Task 12: CREATE PRPs/ai_docs/gemini_api_patterns.md
  - DOCUMENT: Authentication, API calls, error handling, rate limiting
  - INCLUDE: Code examples for Vision and Imagen APIs
  - PLACEMENT: PRPs/ai_docs/

# PHASE 4: CODE ANALYSIS & PARSING

Task 13: CREATE src/imagen_skill/analyzers/parsers/base.py
  - IMPLEMENT: BaseParser abstract class
  - METHODS: find_opportunities(code: str) -> List[Opportunity]
  - PLACEMENT: src/imagen_skill/analyzers/parsers/

Task 14: CREATE src/imagen_skill/analyzers/parsers/patterns.py
  - IMPLEMENT: Regex patterns and heuristics for Qt code
  - PATTERNS: QIcon(), setIcon(), QPixmap(), QLabel with size hints
  - PLACEMENT: src/imagen_skill/analyzers/parsers/

Task 15: CREATE src/imagen_skill/analyzers/parsers/qt_parser.py
  - IMPLEMENT: QtCodeParser class extending BaseParser
  - DETECT: QIcon() empty constructors, QPixmap placeholders, empty QLabel with sizes
  - EXTRACT: Semantic context from variable names (e.g., "settingsButton" -> "settings")
  - SCORE: Confidence based on pattern match quality
  - DEPENDENCIES: Task 13 (BaseParser), Task 14 (Patterns)
  - PLACEMENT: src/imagen_skill/analyzers/parsers/
  - VALIDATION: Test with sample Qt C++ code

Task 16: CREATE src/imagen_skill/analyzers/code_analyzer.py
  - IMPLEMENT: CodeAnalyzer class with async def analyze(files) -> List[Opportunity]
  - DETECT: Framework from file extension and imports
  - DELEGATE: To appropriate parser (QtParser for .cpp/.h files)
  - RANK: Opportunities by confidence score
  - DEPENDENCIES: Task 15 (QtParser), Task 4 (Models)
  - PLACEMENT: src/imagen_skill/analyzers/

Task 17: CREATE tests/unit/test_qt_parser.py
  - IMPLEMENT: Unit tests for QtCodeParser
  - TEST CASES: Detect QIcon(), detect QPixmap(), extract semantic context
  - FIXTURES: Sample Qt code snippets
  - PLACEMENT: tests/unit/

Task 18: CREATE tests/fixtures/sample_code/mainwindow.cpp
  - CREATE: Sample Qt C++ file with various opportunity patterns
  - INCLUDE: Empty QIcon(), QPixmap, QLabel patterns
  - PLACEMENT: tests/fixtures/sample_code/

Task 19: CREATE PRPs/ai_docs/code_parsing_patterns.md
  - DOCUMENT: Qt parsing patterns, heuristics, regex patterns
  - INCLUDE: Examples of each opportunity type
  - PLACEMENT: PRPs/ai_docs/

# PHASE 5: IMAGE GENERATION

Task 20: CREATE src/imagen_skill/generators/prompt_builder.py
  - IMPLEMENT: PromptBuilder class with build_prompt(opportunity, theme) -> str
  - COMBINE: Semantic context + theme colors/style + purpose-specific keywords
  - OPTIMIZE: Prompts for Imagen 3 best practices
  - DEPENDENCIES: Task 4 (Models)
  - PLACEMENT: src/imagen_skill/generators/

Task 21: CREATE src/imagen_skill/generators/background_remover.py
  - IMPLEMENT: BackgroundRemover class with async def remove(image_bytes) -> bytes
  - USE: rembg library with u2net model
  - HANDLE: PIL Image conversions
  - PLACEMENT: src/imagen_skill/generators/

Task 22: CREATE src/imagen_skill/generators/image_generator.py
  - IMPLEMENT: ImageGenerator class with async def generate(opportunity, theme) -> GeneratedImage
  - ORCHESTRATE: Build prompt -> call Imagen -> remove background -> save file
  - DEPENDENCIES: Task 20 (PromptBuilder), Task 21 (BackgroundRemover), Task 8 (GeminiClient)
  - PLACEMENT: src/imagen_skill/generators/
  - VALIDATION: Integration test with mocked API

Task 23: CREATE tests/unit/test_prompt_builder.py
  - IMPLEMENT: Unit tests for PromptBuilder
  - TEST CASES: Icon prompts, logo prompts, background prompts with different themes
  - PLACEMENT: tests/unit/

Task 24: CREATE tests/integration/test_image_generation_flow.py
  - IMPLEMENT: Integration test for full generation pipeline
  - MOCK: Gemini API but test real rembg processing
  - PLACEMENT: tests/integration/

# PHASE 6: CODE INTEGRATION

Task 25: CREATE src/imagen_skill/integrators/frameworks/base.py
  - IMPLEMENT: BaseIntegrator abstract class
  - METHODS: integrate(code, opportunity, image_path) -> str
  - PLACEMENT: src/imagen_skill/integrators/frameworks/

Task 26: CREATE src/imagen_skill/integrators/frameworks/qt_integrator.py
  - IMPLEMENT: QtIntegrator class extending BaseIntegrator
  - REPLACE: QIcon() with QIcon(":/path/to/resource.png")
  - UPDATE: .qrc resource files with new entries
  - VALIDATE: Syntax after changes (basic C++ syntax check)
  - DEPENDENCIES: Task 25 (BaseIntegrator)
  - PLACEMENT: src/imagen_skill/integrators/frameworks/

Task 27: CREATE src/imagen_skill/integrators/asset_manager.py
  - IMPLEMENT: AssetManager class for file placement and naming
  - DETERMINE: Save location based on framework conventions (resources/icons/, etc.)
  - GENERATE: Semantic filenames from context (settings-icon.png)
  - HANDLE: File conflicts (append numbers if needed)
  - PLACEMENT: src/imagen_skill/integrators/

Task 28: CREATE src/imagen_skill/integrators/code_integrator.py
  - IMPLEMENT: CodeIntegrator class with async def integrate(image, opportunity) -> IntegrationResult
  - ORCHESTRATE: Determine save path -> update code -> update resources -> validate
  - GENERATE: Diffs for user review
  - DEPENDENCIES: Task 26 (QtIntegrator), Task 27 (AssetManager)
  - PLACEMENT: src/imagen_skill/integrators/

Task 29: CREATE tests/unit/test_qt_integrator.py
  - IMPLEMENT: Unit tests for QtIntegrator
  - TEST CASES: Replace QIcon(), update .qrc file, handle malformed code
  - PLACEMENT: tests/unit/

Task 30: CREATE PRPs/ai_docs/qt_resource_system.md
  - DOCUMENT: Qt .qrc file format, resource path syntax, integration patterns
  - INCLUDE: Examples of .qrc XML structure
  - PLACEMENT: PRPs/ai_docs/

# PHASE 7: SKILL ORCHESTRATION

Task 31: CREATE src/imagen_skill/core/skill.py
  - IMPLEMENT: ImagenSkill main orchestrator class
  - METHOD: async def execute(target_files, theme_reference, **kwargs) -> SkillResult
  - ORCHESTRATE: Theme analysis -> code analysis -> image generation -> integration
  - PROGRESS: Report progress at each stage
  - ERROR HANDLING: Graceful failure with partial results
  - DEPENDENCIES: All previous tasks
  - PLACEMENT: src/imagen_skill/core/

Task 32: CREATE src/imagen_skill/main.py
  - IMPLEMENT: CLI entry point and skill invocation interface
  - ARGUMENT PARSING: Accept target files, theme reference, options
  - OUTPUT: Formatted results report
  - DEPENDENCIES: Task 31 (ImagenSkill)
  - PLACEMENT: src/imagen_skill/

Task 33: CREATE tests/integration/test_end_to_end.py
  - IMPLEMENT: Full end-to-end test with mocked APIs
  - TEST FLOW: Theme reference + Qt file -> complete integration
  - MOCK: All external APIs (Gemini, file writes)
  - PLACEMENT: tests/integration/

# PHASE 8: TESTING & VALIDATION

Task 34: CREATE tests/conftest.py
  - IMPLEMENT: Shared pytest fixtures
  - FIXTURES: mock_gemini_client, sample_theme, sample_opportunities, mock_config
  - PLACEMENT: tests/

Task 35: CREATE .env.example
  - DOCUMENT: Required environment variables
  - INCLUDE: GOOGLE_API_KEY, LOG_LEVEL, DEBUG
  - PLACEMENT: Root directory

Task 36: CREATE README.md
  - DOCUMENT: Installation, usage, configuration, examples
  - INCLUDE: Quick start guide
  - PLACEMENT: Root directory

Task 37: RUN all validation levels
  - LEVEL 1: ruff check src/ --fix && mypy src/ && ruff format src/
  - LEVEL 2: pytest tests/unit/ -v
  - LEVEL 3: pytest tests/integration/ -v
  - LEVEL 4: pytest tests/ --cov=src/imagen_skill --cov-report=term-missing
  - EXPECTED: All pass with 80%+ coverage

Task 38: CREATE docs/architecture.md
  - DOCUMENT: System architecture, component interactions, data flow
  - PLACEMENT: docs/
```

### Implementation Patterns & Key Details

```python
# PATTERN: Async API Client
class GeminiClient:
    """Async client for Gemini API."""

    def __init__(self, config: Config):
        self.api_key = config.google_api_key
        self.timeout = config.timeout
        self.max_retries = config.max_retries
        genai.configure(api_key=self.api_key)
        self.vision_model = genai.GenerativeModel('gemini-1.5-pro')
        self.imagen_model = genai.ImageGenerationModel('imagen-3.0-generate-002')

    async def analyze_image_vision(self, image_path: Path, prompt: str) -> Dict:
        """Analyze image using Gemini Vision with structured output."""
        import asyncio
        from PIL import Image

        image = Image.open(image_path)

        # Use structured output for JSON response
        generation_config = genai.GenerationConfig(
            response_mime_type="application/json",
            temperature=0.2  # Lower temp for more consistent extraction
        )

        # Run in executor since genai is sync
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.vision_model.generate_content(
                [prompt, image],
                generation_config=generation_config
            )
        )

        return json.loads(response.text)

    async def generate_image(self, prompt: str, aspect_ratio: str = "1:1") -> bytes:
        """Generate image using Imagen 3."""
        import asyncio

        # GOTCHA: Imagen API is synchronous, wrap in executor
        loop = asyncio.get_event_loop()

        for attempt in range(self.max_retries):
            try:
                response = await loop.run_in_executor(
                    None,
                    lambda: self.imagen_model.generate_images(
                        prompt=prompt,
                        aspect_ratio=aspect_ratio,
                        number_of_images=1,
                        safety_filter_level="block_medium_and_above"
                    )
                )

                # CRITICAL: Extract image bytes from response
                image_bytes = response.images[0]._pil_image.tobytes()
                return image_bytes

            except Exception as e:
                if "429" in str(e) and attempt < self.max_retries - 1:
                    # Rate limited, exponential backoff
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise APIError(f"Image generation failed: {e}")

# PATTERN: Theme Analysis with Structured Output
class ThemeAnalyzer:
    """Extract visual theme from reference images."""

    def __init__(self, gemini_client: GeminiClient):
        self.client = gemini_client

    async def analyze(self, image_path: Path) -> ThemeProfile:
        """Analyze theme from reference image."""

        prompt = """
        Analyze this UI design/screenshot and extract theme information.

        Return JSON with this exact structure:
        {
            "colors": {
                "primary": "#RRGGBB",
                "secondary": ["#RRGGBB", ...],
                "accent": ["#RRGGBB", ...],
                "background": "#RRGGBB",
                "text": "#RRGGBB"
            },
            "style": {
                "aesthetic": "modern minimal|retro|playful|professional|etc",
                "mood": "serious|playful|elegant|technical|etc",
                "keywords": ["clean", "rounded", "shadow", ...],
                "icon_style": "outline|filled|flat|3d|null"
            },
            "patterns": ["rounded corners", "drop shadows", "gradients", ...]
        }

        Extract dominant and accent colors, identify visual style keywords,
        and note common design patterns.
        """

        theme_data = await self.client.analyze_image_vision(image_path, prompt)

        # CRITICAL: Validate and parse into ThemeProfile model
        return ThemeProfile(**theme_data)

# PATTERN: Qt Code Parsing with Regex
class QtCodeParser(BaseParser):
    """Parse Qt C++ code to find image opportunities."""

    # CRITICAL: Patterns for Qt opportunity detection
    PATTERNS = {
        'empty_qicon': r'(\w+)\.setIcon\(QIcon\(\)\)',
        'empty_qpixmap': r'QPixmap\s+(\w+);',
        'placeholder_path': r'QPixmap\(["\'](?:placeholder|temp|todo)["\']',
        'sized_qlabel': r'QLabel\s*\*\s*(\w+).*?setFixedSize\((\d+),\s*(\d+)\)',
    }

    def find_opportunities(self, code: str, file_path: Path) -> List[Opportunity]:
        """Find UI enhancement opportunities in Qt code."""
        opportunities = []

        # Pattern: button.setIcon(QIcon())
        for match in re.finditer(self.PATTERNS['empty_qicon'], code):
            var_name = match.group(1)
            line_num = code[:match.start()].count('\n') + 1

            # Extract semantic meaning from variable name
            semantic = self._extract_semantic(var_name)  # "settingsButton" -> "settings"

            opportunities.append(Opportunity(
                location=CodeLocation(file_path=file_path, line_number=line_num),
                purpose=ImagePurpose.ICON,
                semantic_context=semantic,
                code_snippet=match.group(0),
                integration_type=IntegrationType.QT_ICON,
                confidence=0.9,  # High confidence for explicit QIcon()
                size_hint="32x32",  # Default icon size
                framework=Framework.QT
            ))

        return opportunities

    def _extract_semantic(self, var_name: str) -> str:
        """Extract semantic meaning from variable name."""
        # PATTERN: settingsButton -> settings, profileIcon -> profile
        semantic = re.sub(r'(Button|Icon|Pixmap|Label|Widget)$', '', var_name)
        # Convert camelCase to lowercase
        semantic = re.sub(r'([A-Z])', r' \1', semantic).strip().lower()
        return semantic or "unknown"

# PATTERN: Prompt Building from Context + Theme
class PromptBuilder:
    """Build Imagen prompts from opportunity context and theme."""

    def build_prompt(self, opportunity: Opportunity, theme: ThemeProfile) -> str:
        """Combine context and theme into optimal Imagen prompt."""

        # Base description from semantic context
        description = opportunity.semantic_context

        # Purpose-specific framing
        purpose_templates = {
            ImagePurpose.ICON: f"{description} icon",
            ImagePurpose.LOGO: f"{description} logo design",
            ImagePurpose.BUTTON: f"{description} button graphic",
            ImagePurpose.BACKGROUND: f"{description} background pattern",
        }
        base = purpose_templates.get(opportunity.purpose, description)

        # Apply theme styling
        style = theme.style.aesthetic
        primary_color = theme.colors.primary
        keywords = ", ".join(theme.style.keywords[:3])  # Top 3 keywords

        # Build full prompt
        prompt = f"""
        {base}, {style} style,
        using {primary_color} as primary color,
        {keywords},
        high quality, professional design
        """

        # CRITICAL: Add background requirement for icons/logos (for easy removal)
        if opportunity.purpose in [ImagePurpose.ICON, ImagePurpose.LOGO]:
            prompt += ", on solid white background for easy removal"

        return prompt.strip()

# PATTERN: Qt Code Integration
class QtIntegrator(BaseIntegrator):
    """Integrate images into Qt C++ code."""

    def integrate(self, code: str, opportunity: Opportunity, image_path: Path) -> str:
        """Update Qt code with image reference."""

        # Convert file path to Qt resource path
        # /project/resources/icons/settings.png -> :/resources/icons/settings.png
        resource_path = self._to_resource_path(image_path)

        lines = code.split('\n')
        target_line = lines[opportunity.location.line_number - 1]

        if opportunity.integration_type == IntegrationType.QT_ICON:
            # Replace: button.setIcon(QIcon())
            # With: button.setIcon(QIcon(":/resources/icons/settings.png"))
            updated_line = re.sub(
                r'QIcon\(\)',
                f'QIcon("{resource_path}")',
                target_line
            )
        elif opportunity.integration_type == IntegrationType.QT_PIXMAP:
            # Replace: QPixmap pixmap;
            # With: QPixmap pixmap(":/resources/images/logo.png");
            updated_line = re.sub(
                r'QPixmap\s+(\w+);',
                f'QPixmap \\1("{resource_path}");',
                target_line
            )

        lines[opportunity.location.line_number - 1] = updated_line
        return '\n'.join(lines)

    def update_qrc_file(self, qrc_path: Path, resource_path: Path) -> None:
        """Add resource entry to .qrc file."""
        # CRITICAL: Qt .qrc files are XML format
        # <RCC>
        #   <qresource prefix="/">
        #     <file>resources/icons/settings.png</file>
        #   </qresource>
        # </RCC>

        import xml.etree.ElementTree as ET

        tree = ET.parse(qrc_path)
        root = tree.getroot()

        # Find or create qresource element
        qresource = root.find('qresource')
        if qresource is None:
            qresource = ET.SubElement(root, 'qresource', prefix='/')

        # Add file entry
        file_elem = ET.SubElement(qresource, 'file')
        file_elem.text = str(resource_path)

        tree.write(qrc_path, encoding='utf-8', xml_declaration=True)
```

### Integration Points

```yaml
ENVIRONMENT:
  - variable: GOOGLE_API_KEY
    required: true
    description: "Google Gemini API key for Vision and Imagen access"
    example: "export GOOGLE_API_KEY='your-key-here'"

  - variable: LOG_LEVEL
    required: false
    default: "INFO"
    description: "Logging level (DEBUG, INFO, WARNING, ERROR)"

  - variable: DEBUG
    required: false
    default: "false"
    description: "Enable debug mode with verbose output"

FILE_SYSTEM:
  - action: "Create resources directory structure"
    pattern: "resources/icons/, resources/images/, resources/ui/"
    when: "First time integration in new project"

  - action: "Create or update .qrc file"
    pattern: "resources.qrc in Qt project root"
    when: "Adding Qt resources"

EXTERNAL_APIs:
  - service: "Google Gemini Vision API"
    endpoint: "Via google-generativeai SDK"
    rate_limit: "15 requests per minute"
    cost: "~$0.01 per image analysis"

  - service: "Google Imagen 3 API"
    endpoint: "Via google-generativeai SDK"
    rate_limit: "Varies by quota"
    cost: "~$0.03-0.04 per image generation"
```

## Validation Loop

### Level 1: Syntax & Style (Immediate Feedback)

```bash
# Run after each file creation
ruff check src/imagen_skill/ --fix
mypy src/imagen_skill/
ruff format src/imagen_skill/

# Expected: Zero errors. Fix any issues before proceeding.
```

### Level 2: Unit Tests (Component Validation)

```bash
# Test each component as created
pytest tests/unit/ -v --tb=short

# Test with coverage
pytest tests/unit/ --cov=src/imagen_skill --cov-report=term-missing

# Expected: All tests pass, 80%+ coverage for tested modules
```

### Level 3: Integration Testing (System Validation)

```bash
# Run integration tests with mocked external APIs
pytest tests/integration/ -v

# Test end-to-end flow
pytest tests/integration/test_end_to_end.py -v -s

# Expected: Complete workflow succeeds with mocked APIs
```

### Level 4: Manual Validation (Real API Testing)

```bash
# CRITICAL: Requires GOOGLE_API_KEY in environment
export GOOGLE_API_KEY='your-api-key-here'

# Test theme analysis with real image
python -m imagen_skill.main analyze-theme tests/fixtures/sample_images/theme_reference.png

# Test full workflow with real Qt file
python -m imagen_skill.main enhance \
  --theme tests/fixtures/sample_images/theme_reference.png \
  --files tests/fixtures/sample_code/mainwindow.cpp \
  --dry-run

# Expected: Successful analysis and generation reports, costs logged
```

## Final Validation Checklist

### Technical Validation

- [ ] All 4 validation levels completed successfully
- [ ] All tests pass: `pytest tests/ -v` (100% pass rate)
- [ ] No linting errors: `ruff check src/imagen_skill/` (0 errors)
- [ ] No type errors: `mypy src/imagen_skill/` (0 errors)
- [ ] No formatting issues: `ruff format src/imagen_skill/ --check` (consistent)
- [ ] Test coverage: `pytest --cov=src/imagen_skill` (80%+ coverage)

### Feature Validation

- [ ] Theme analyzer extracts colors and styles from reference images
- [ ] Code analyzer detects 3+ opportunity types in Qt code (QIcon, QPixmap, QLabel)
- [ ] Image generator produces images matching theme
- [ ] Background remover creates transparent PNGs for icons
- [ ] Code integrator updates Qt files without syntax errors
- [ ] Qt .qrc files updated correctly with new resources
- [ ] End-to-end workflow completes in <60 seconds for 5 images
- [ ] Cost tracking accurate and stays under $0.50 per session
- [ ] Progress reporting clear and informative

### Code Quality Validation

- [ ] Follows Python project structure best practices (src-layout)
- [ ] All models use Pydantic v2 with proper validation
- [ ] Async/await used consistently for I/O operations
- [ ] Error handling comprehensive with custom exceptions
- [ ] Logging informative with structured output
- [ ] File placement matches desired directory structure
- [ ] Dependencies properly managed in pyproject.toml

### Documentation & Deployment

- [ ] README.md complete with installation and usage instructions
- [ ] PRPs/ai_docs/ populated with Gemini, parsing, Qt resource docs
- [ ] Architecture documented in docs/architecture.md
- [ ] .env.example provided with all required variables
- [ ] Example fixtures available for testing

---

## Anti-Patterns to Avoid

- ❌ Don't use synchronous API calls - wrap in async/await or executor
- ❌ Don't hardcode API keys - use environment variables and Config
- ❌ Don't skip validation - always validate with Pydantic models
- ❌ Don't ignore rate limits - implement exponential backoff
- ❌ Don't modify files without validation - check syntax before writing
- ❌ Don't use generic error messages - provide specific context
- ❌ Don't skip tests - achieve 80%+ coverage
- ❌ Don't use requests library - use httpx for async support
- ❌ Don't hardcode file paths - use pathlib.Path
- ❌ Don't skip type hints - maintain strict mypy compliance

---

## Success Metrics

**Confidence Score for One-Pass Implementation**: 8/10

**Rationale**: This PRP provides:
- ✅ Complete PRD with detailed requirements
- ✅ Comprehensive Python project structure guidance
- ✅ Detailed implementation tasks with dependencies
- ✅ Code patterns and examples for all major components
- ✅ External API integration guidance
- ✅ Complete validation approach
- ✅ Type safety with Pydantic models
- ⚠️ Requires external research for specific Gemini API details
- ⚠️ Qt .qrc file handling may need additional reference

**Areas requiring additional research during implementation**:
1. Specific Gemini Imagen 3 API response format details
2. Qt .qrc XML manipulation edge cases
3. rembg model selection and optimization

**Time Estimate**: 3-4 weeks for full Phase 1 implementation (Qt support only)
