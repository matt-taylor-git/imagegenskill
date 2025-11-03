"""Regex patterns for detecting UI opportunities in code."""

import re

# Qt C++ Patterns
QT_PATTERNS = {
    # button.setIcon(QIcon())
    "empty_qicon": re.compile(r"(\w+)\.setIcon\(QIcon\(\)\)"),
    # QPixmap pixmap;
    "empty_qpixmap": re.compile(r"QPixmap\s+(\w+)\s*;"),
    # QPixmap("placeholder.png") or QPixmap("temp.png")
    "placeholder_path": re.compile(r'QPixmap\s*\(\s*["\'](?:placeholder|temp|todo|empty)["\']'),
    # QLabel *label; label->setFixedSize(32, 32);
    "sized_qlabel": re.compile(
        r"QLabel\s*\*?\s*(\w+).*?setFixedSize\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)"
    ),
    # QIcon("")
    "empty_qicon_string": re.compile(r'QIcon\s*\(\s*["\']\s*["\']\s*\)'),
    # setWindowIcon(QIcon())
    "window_icon": re.compile(r"setWindowIcon\s*\(\s*QIcon\s*\(\s*\)\s*\)"),
}

# React/JSX Patterns
REACT_PATTERNS = {
    # <img src="placeholder.png" />
    "placeholder_img": re.compile(
        r'<img\s+[^>]*src\s*=\s*["\'](?:placeholder|temp|todo)["\'][^>]*>'
    ),
    # <div className="icon"></div> (empty icon container)
    "empty_icon_div": re.compile(
        r'<div\s+[^>]*className\s*=\s*["\'][^"\']*icon[^"\']*["\'][^>]*>\s*</div>'
    ),
    # const Icon = null;
    "null_icon": re.compile(r"const\s+(\w*[Ii]con\w*)\s*=\s*null"),
}

# HTML Patterns
HTML_PATTERNS = {
    # <img src="">
    "empty_src": re.compile(r'<img\s+[^>]*src\s*=\s*["\']["\']'),
    # <div class="icon"></div>
    "empty_icon": re.compile(r'<div\s+class\s*=\s*["\']icon["\']>\s*</div>'),
}

# Unity C# Patterns
UNITY_PATTERNS = {
    # public Sprite icon;
    "public_sprite": re.compile(r"public\s+Sprite\s+(\w+)\s*;"),
    # image.sprite = null;
    "null_sprite": re.compile(r"(\w+)\.sprite\s*=\s*null"),
}
