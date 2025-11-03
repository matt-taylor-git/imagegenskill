# Gemini API Patterns for Imagen Skill

## Authentication

```python
from google import genai

# Configure with API key
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
```

## Gemini Vision for Theme Analysis

### Structured JSON Output

```python
from google.genai.types import GenerateContentConfig
from PIL import Image
import json

# Load image
image = Image.open("theme.png")

# Configure for JSON response
config = GenerateContentConfig(
    response_mime_type="application/json",
    temperature=0.2,  # Lower for consistency
)

# Generate with structured output
response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents=[prompt, image],
    config=config,
)

# Parse JSON
result = json.loads(response.text)
```

### Theme Extraction Prompt Pattern

```python
prompt = """
Analyze this UI and return JSON with:
{
    "colors": {
        "primary": "#RRGGBB",
        "secondary": ["#RRGGBB"],
        "accent": ["#RRGGBB"],
        "background": "#RRGGBB",
        "text": "#RRGGBB"
    },
    "style": {
        "aesthetic": "modern minimal|retro|playful",
        "mood": "professional|casual|technical",
        "keywords": ["clean", "rounded"],
        "icon_style": "outline|filled|null"
    },
    "patterns": ["rounded corners", "shadows"]
}
"""
```

## Imagen 3 for Image Generation

### Basic Generation

```python
from google.genai.types import GenerateImagesConfig

config = GenerateImagesConfig(
    number_of_images=1,
    aspect_ratio="1:1",  # "1:1", "16:9", "9:16", "4:3", "3:4"
    safety_filter_level="block_medium_and_above",
)

response = client.models.generate_images(
    model="imagen-3.0-generate-002",
    prompt="Settings icon, modern minimal style, blue accent",
    config=config,
)

# Extract image bytes
generated_image = response.generated_images[0]
image_bytes = generated_image.image.tobytes()
```

### Async Wrapper Pattern

```python
import asyncio

async def generate_image_async(client, prompt, aspect_ratio="1:1"):
    """Wrap synchronous Imagen call in executor."""
    loop = asyncio.get_event_loop()

    response = await loop.run_in_executor(
        None,
        lambda: client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=prompt,
            config=GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio=aspect_ratio,
            ),
        ),
    )

    return response.generated_images[0].image
```

## Error Handling

### Rate Limiting (429)

```python
async def generate_with_retry(client, prompt, max_retries=3):
    """Generate with exponential backoff on rate limits."""
    for attempt in range(max_retries):
        try:
            return await generate_image_async(client, prompt)
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                wait_time = 2 ** attempt
                await asyncio.sleep(wait_time)
                continue
            raise
```

### Safety Filter Blocks

```python
try:
    response = client.models.generate_images(...)
except Exception as e:
    if "safety" in str(e).lower():
        # Image blocked by safety filter
        logger.warning(f"Image blocked by safety filter: {prompt}")
        # Adjust prompt or skip
```

## Best Practices

1. **Use structured output** for consistent theme extraction
2. **Lower temperature (0.2)** for theme analysis
3. **Wrap in asyncio.run_in_executor** since genai is synchronous
4. **Implement retry logic** for 429 rate limits
5. **Add white backgrounds** to prompts for easy background removal
6. **Keep prompts under 480 tokens** for Imagen
7. **Use specific model versions** not "latest" for consistency
