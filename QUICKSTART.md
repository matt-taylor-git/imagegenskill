# Imagen Skill - Quick Start Guide

Get up and running with the Imagen UI Enhancement Skill for Claude Code in 5 minutes.

## Prerequisites

- **Claude Code** installed and configured
- **Python 3.10-3.13** installed
- **Google Gemini API key** ([Get one free here](https://aistudio.google.com/app/apikey))

## Step 1: Get Your Google API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key (starts with `AIza...`)
4. Keep it handy - you'll need it in Step 3

## Step 2: Install the Skill

### Option A: Install as Claude Code Skill (Recommended)

```bash
# Navigate to your Claude Code skills directory
cd ~/.claude/skills/  # On macOS/Linux
# OR
cd %USERPROFILE%\.claude\skills\  # On Windows

# Clone the skill
git clone <this-repository-url> imagen-skill
cd imagen-skill

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -e ".[dev]"
```

### Option B: Install Standalone

```bash
# Clone anywhere
git clone <this-repository-url>
cd imagegenskill

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# OR venv\Scripts\activate  # Windows

# Install dependencies
pip install -e ".[dev]"
```

## Step 3: Configure API Key

Create a `.env` file in the skill directory:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# (Use your favorite text editor)
```

Edit the `.env` file:
```bash
GOOGLE_API_KEY=AIza...your-actual-api-key-here...
```

**Important**: Never commit your `.env` file to version control!

## Step 4: Verify Installation

Test that everything works:

```bash
# Quick test (should show help)
imagen-skill --help

# Should output:
# usage: imagen-skill [-h] [--theme THEME] ...
```

## Step 5: First Run - Try It Out!

### Create a Test Qt File

Create `test_mainwindow.cpp`:

```cpp
#include <QApplication>
#include <QPushButton>
#include <QIcon>
#include <QMainWindow>

class MainWindow : public QMainWindow {
public:
    MainWindow() {
        // Empty icons - Imagen skill will fill these!
        QPushButton *settingsBtn = new QPushButton("Settings");
        settingsBtn->setIcon(QIcon());

        QPushButton *profileBtn = new QPushButton("Profile");
        profileBtn->setIcon(QIcon());

        QPushButton *helpBtn = new QPushButton("Help");
        helpBtn->setIcon(QIcon());
    }
};
```

### Create a Theme Reference (or use a screenshot)

Option 1: Use an existing screenshot of your app
Option 2: Create a simple reference image with your brand colors

### Run the Skill!

```bash
# Dry run first (preview without changes)
imagen-skill test_mainwindow.cpp \
  --theme path/to/your-theme-image.png \
  --dry-run

# If it looks good, run for real
imagen-skill test_mainwindow.cpp \
  --theme path/to/your-theme-image.png
```

### What Happens:

1. **Theme Analysis**: Extracts colors and style from your theme image
2. **Code Analysis**: Finds empty `QIcon()` calls in your C++ file
3. **Image Generation**: Creates 3 themed icons (settings, profile, help)
4. **Integration**: Updates your code with the new icons
5. **Resource Files**: Creates/updates `resources.qrc`

Expected output:
```
=============================================================
Imagen UI Enhancement Skill - Starting
=============================================================
Phase 1: Analyzing theme from theme-image.png
  Theme: modern minimal, Primary: #3B82F6
Phase 2: Analyzing 1 code file(s)
  Found 3 opportunities
Phase 3: Generating 3 image(s)
  [1/3] Generating icon for 'settings'
  [2/3] Generating icon for 'profile'
  [3/3] Generating icon for 'help'
  Generated 3 image(s)
Phase 4: Integrating into code (dry_run=False)
  [1/3] Integrating settings-icon.png
  [2/3] Integrating profile-icon.png
  [3/3] Integrating help-icon.png
=============================================================
Execution Summary
=============================================================
  Opportunities found:      3
  Images generated:         3
  Integrations completed:   3
  Files modified:           1
  Total cost:               $0.09
  Processing time:          12.3s
=============================================================
```

## Step 6: Using with Claude Code

### Method 1: Direct Invocation

In Claude Code chat, you can now say:

```
"Please run the imagen skill on my mainwindow.cpp file.
Use theme-screenshot.png as the theme reference."
```

Claude Code will detect the skill and invoke it automatically.

### Method 2: Create a Slash Command (Optional)

Create `.claude/commands/enhance-ui.md`:

```markdown
Please analyze {{file}} for UI enhancement opportunities and generate themed images.

Steps:
1. Run: cd ~/.claude/skills/imagen-skill && source venv/bin/activate
2. Execute: imagen-skill {{file}} --theme {{theme}} {{flags}}
3. Report the results and show what was modified
```

Then use:
```
/enhance-ui file=mainwindow.cpp theme=theme.png
```

## Common Issues & Solutions

### Issue: "Cannot find implementation or library stub for module named 'google'"

**Solution**: Activate your virtual environment first!
```bash
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows
```

### Issue: "Error: GOOGLE_API_KEY not found"

**Solution**: Make sure `.env` file exists and contains your API key:
```bash
# Check if .env exists
ls -la .env

# Check contents (safely)
grep GOOGLE_API_KEY .env
```

### Issue: "Rate limited (429 error)"

**Solution**: The skill automatically retries. If it persists:
- Wait a few minutes
- Reduce `--max-images` to generate fewer images at once
- Check your API quota at [Google AI Studio](https://aistudio.google.com/)

### Issue: "No opportunities found"

**Solution**:
- Ensure your code has patterns the skill recognizes
- For Qt: Look for `QIcon()`, `QPixmap()`, `setIcon()` patterns
- Use `--debug` flag to see detailed analysis:
  ```bash
  imagen-skill myfile.cpp --theme theme.png --debug
  ```

## Advanced Usage

### Limit Cost Per Session

```bash
# Set in .env
MAX_COST_PER_SESSION=0.25  # Stop after $0.25
```

### Generate Only a Few Images

```bash
imagen-skill myfile.cpp --theme theme.png --max-images 2
```

### Multiple Files at Once

```bash
imagen-skill src/*.cpp --theme theme.png --project-root .
```

### Preview Without Making Changes

```bash
imagen-skill myfile.cpp --theme theme.png --dry-run
```

### Enable Debug Logging

```bash
imagen-skill myfile.cpp --theme theme.png --debug
```

## What Gets Created

After running the skill, you'll find:

```
your-project/
├── resources/              # Created automatically
│   └── icons/
│       ├── settings-icon.png
│       ├── profile-icon.png
│       └── help-icon.png
├── resources.qrc           # Created or updated
└── mainwindow.cpp          # Updated with icon references
```

Your code changes from:
```cpp
settingsBtn->setIcon(QIcon());
```

To:
```cpp
settingsBtn->setIcon(QIcon(":/resources/icons/settings-icon.png"));
```

## Cost Expectations

- **Theme analysis**: ~$0.01 per image
- **Image generation**: ~$0.03-0.04 per image
- **Typical session** (5 icons): ~$0.15-0.20
- **Free tier**: 15 requests/minute, 1500 requests/day

## Next Steps

1. **Try it on your real project**: Point it at your actual Qt files
2. **Customize themes**: Use different reference images for different moods
3. **Batch process**: Run on multiple files to quickly polish your entire UI
4. **Integrate into workflow**: Add to your Claude Code slash commands

## Getting Help

- **Documentation**: See `README.md` for full details
- **Examples**: Check `PRPs/imagen-skill-prd-v2.md` for use cases
- **Issues**: Report bugs on GitHub (if available)
- **API Docs**: [Google Gemini Docs](https://ai.google.dev/gemini-api/docs)

## Tips for Best Results

1. **Theme References**:
   - Use clear screenshots showing your app's visual style
   - Include multiple UI elements so the skill can extract patterns
   - Higher resolution = better theme extraction

2. **Semantic Variable Names**:
   - Use descriptive names: `settingsButton` → generates "settings" icon
   - Avoid generic names: `button1` → generates generic icons

3. **Review Generated Images**:
   - Always review before committing
   - Regenerate if needed with different prompts/themes
   - Images are saved as PNG files - easy to replace manually

4. **Start Small**:
   - Try 2-3 icons first before batch processing
   - Use `--dry-run` to preview
   - Check costs with `--max-images 1`

---

**Ready to enhance your UI? Run your first command now!** 🚀

```bash
imagen-skill your-file.cpp --theme your-theme.png --dry-run
```
