# Code Parsing Patterns

## Qt C++ Pattern Detection

### Pattern 1: Empty QIcon()

```cpp
// Detect this:
settingsButton.setIcon(QIcon());

// Pattern:
(\w+)\.setIcon\(QIcon\(\)\)

// Extract:
- Variable name: settingsButton
- Semantic: "settings" (remove Button suffix)
- Confidence: 0.9 (explicit)
```

### Pattern 2: Empty QIcon String

```cpp
// Detect:
QIcon("")
QIcon icon("");

// Pattern:
QIcon\s*\(\s*["\']["\']\\s*\)

// Confidence: 0.85
```

### Pattern 3: Window Icons

```cpp
// Detect:
setWindowIcon(QIcon());

// Pattern:
setWindowIcon\s*\(\s*QIcon\s*\(\s*\)\s*\)

// Semantic: "application window"
// Confidence: 0.95 (specific API)
```

### Pattern 4: Uninitialized QPixmap

```cpp
// Detect:
QPixmap logoPixmap;

// Pattern:
QPixmap\s+(\w+)\s*;

// Semantic: Extract from variable name
// Confidence: 0.7 (might be intentional)
```

### Pattern 5: Placeholder Paths

```cpp
// Detect:
QPixmap("placeholder.png")
QPixmap("temp.png")
QPixmap("todo.png")

// Pattern:
QPixmap\s*\(["\'](?:placeholder|temp|todo|empty)["\']\)

// Confidence: 0.95 (explicitly marked)
```

## Semantic Extraction

```python
def extract_semantic(var_name: str) -> str:
    """Extract meaning from variable names."""
    # Remove common suffixes
    semantic = re.sub(
        r'(Button|Icon|Pixmap|Label|Widget|Image|Sprite|Btn|Img)$',
        '',
        var_name,
        flags=re.IGNORECASE
    )

    # Convert camelCase to spaces
    semantic = re.sub(r'([A-Z])', r' \1', semantic).strip().lower()

    return semantic or "unknown"

# Examples:
# settingsButton -> "settings"
# profileIcon -> "profile"
# mainWindowLogo -> "main window logo"
```

## Confidence Scoring

```python
confidence_rules = {
    "explicit_placeholder": 0.95,  # QPixmap("placeholder.png")
    "window_icon_api": 0.95,       # setWindowIcon(QIcon())
    "empty_qicon": 0.90,           # button.setIcon(QIcon())
    "empty_string": 0.85,          # QIcon("")
    "uninitialized": 0.70,         # QPixmap var;
}
```

## Line Number Extraction

```python
def get_line_number(code: str, match_start: int) -> int:
    """Get line number from match position."""
    return code[:match_start].count('\n') + 1
```

## Context Extraction

```python
def get_line_context(code: str, match_start: int, match_end: int) -> str:
    """Extract full line containing match."""
    line_start = code.rfind('\n', 0, match_start) + 1
    line_end = code.find('\n', match_end)
    if line_end == -1:
        line_end = len(code)

    return code[line_start:line_end]
```

## Future Framework Patterns

### React/JSX

```jsx
// Detect:
<img src="placeholder.png" />
<div className="icon"></div>
const Icon = null;

// Patterns:
<img\s+[^>]*src\s*=\s*["\'](?:placeholder|temp)["\']
<div\s+[^>]*className\s*=\s*["\'][^"\']*icon[^"\']*["\'][^>]*>\s*</div>
const\s+(\w*[Ii]con\w*)\s*=\s*null
```

### Unity C#

```csharp
// Detect:
public Sprite iconSprite;
image.sprite = null;

// Patterns:
public\s+Sprite\s+(\w+)\s*;
(\w+)\.sprite\s*=\s*null
```
