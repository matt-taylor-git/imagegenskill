# Qt Resource System (.qrc)

## Overview

Qt uses `.qrc` (Qt Resource Collection) XML files to embed resources into the application binary.

## .qrc File Format

```xml
<!DOCTYPE RCC>
<RCC version="1.0">
    <qresource prefix="/">
        <file>resources/icons/settings.png</file>
        <file>resources/icons/profile.png</file>
        <file>resources/images/logo.png</file>
    </qresource>
</RCC>
```

## Resource Path Syntax

In C++ code, resources are referenced with `:` prefix:

```cpp
// Load icon from resources
QIcon icon(":/resources/icons/settings.png");

// Load pixmap
QPixmap pixmap(":/resources/images/logo.png");

// The ":" prefix indicates a Qt resource path
```

## Adding Resources Programmatically

```python
import xml.etree.ElementTree as ET

def add_to_qrc(qrc_path: Path, resource_path: Path):
    """Add resource entry to .qrc file."""

    # Parse or create
    if qrc_path.exists():
        tree = ET.parse(qrc_path)
        root = tree.getroot()
    else:
        root = ET.Element("RCC", version="1.0")
        tree = ET.ElementTree(root)

    # Find or create qresource
    qresource = root.find("qresource")
    if qresource is None:
        qresource = ET.SubElement(root, "qresource", prefix="/")

    # Check if already exists
    resource_str = str(resource_path).replace("\\", "/")
    for file_elem in qresource.findall("file"):
        if file_elem.text == resource_str:
            return  # Already exists

    # Add file entry
    file_elem = ET.SubElement(qresource, "file")
    file_elem.text = resource_str

    # Write back
    tree.write(qrc_path, encoding="utf-8", xml_declaration=True)
```

## Directory Structure Conventions

```
project/
├── resources/
│   ├── icons/          # Icons (16x16, 32x32, 64x64)
│   ├── images/         # General images
│   ├── ui/
│   │   └── buttons/    # Button graphics
│   └── backgrounds/    # Background images
├── resources.qrc       # Resource collection file
└── src/
    └── mainwindow.cpp
```

## Converting Filesystem Path to Resource Path

```python
def to_qt_resource_path(file_path: Path) -> str:
    """Convert filesystem path to Qt resource path.

    Examples:
        /project/resources/icons/settings.png -> :/resources/icons/settings.png
        resources/icons/settings.png -> :/resources/icons/settings.png
    """
    parts = file_path.parts

    # Find 'resources' in path
    try:
        res_idx = parts.index("resources")
        rel_path = "/".join(parts[res_idx:])
    except ValueError:
        # No 'resources' directory, use filename
        rel_path = f"resources/{file_path.name}"

    return f":/{rel_path}"
```

## Integration Pattern

1. **Generate image** -> Save to `resources/icons/settings.png`
2. **Update .qrc** -> Add `<file>resources/icons/settings.png</file>`
3. **Update C++ code** -> Change `QIcon()` to `QIcon(":/resources/icons/settings.png")`
4. **Compile resources** -> Qt build system compiles .qrc into binary

## Build System Integration

### qmake (.pro file)

```qmake
RESOURCES += resources.qrc
```

### CMake

```cmake
qt5_add_resources(RESOURCES resources.qrc)
add_executable(myapp ${SOURCES} ${RESOURCES})
```

## Common Gotchas

1. **Paths must be relative** to .qrc file location
2. **Use forward slashes** even on Windows in .qrc files
3. **Resources are read-only** at runtime
4. **Recompile required** after .qrc changes
5. **Large files increase binary size** - consider external resources for large assets
