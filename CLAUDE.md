# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **PRP (Product Requirement Prompt) Framework** repository designed to orchestrate AI coding agents (specifically Claude Code) through structured, context-rich implementation workflows. PRPs are structured prompts that provide everything an AI agent needs to deliver working software: context, implementation details, validation gates, and execution guidance.

**Key Philosophy**: "Over-specifying what to build while under-specifying the context is why so many AI-driven coding attempts stall at 80%." PRPs fix this by combining disciplined scope with comprehensive context.

## Architecture

### Directory Structure

```
.
├── .claude/                    # Claude Code slash commands
│   ├── development/           # General development commands (commits, PRs, debugging)
│   ├── prp-core/             # Core PRP workflow commands (create, execute, review)
│   ├── prp-commands/         # Specialized PRP types (spec, task, story, POC)
│   ├── typescript/           # TypeScript-specific commands
│   ├── code-quality/         # Code review and quality commands
│   ├── git-operations/       # Git workflow commands
│   └── rapid-development/    # Experimental rapid dev patterns
│
├── PRPs/                      # PRP templates and documentation
│   ├── prp_base.md           # Base PRP template (comprehensive, implementation-focused)
│   ├── prp_planning.md       # Planning PRP for PRD generation with diagrams
│   ├── prp_task.md           # Task-focused PRP template
│   ├── prp_spec.md           # Specification template (inspired by IndyDevDan)
│   ├── prp_story_task.md     # User story/task template
│   ├── prp_poc_react.md      # React POC template
│   ├── ai_docs/              # Library documentation for context injection
│   └── scripts/
│       └── prp_runner.py     # Python script to run PRPs with Claude Code
│
└── PRPs/completed/            # Completed PRPs (moved here after execution)
```

### Core Concepts

**PRP Structure** (from `prp_base.md`):
1. **Context**: Precise file paths, library versions, code snippets, examples
2. **Implementation Details**: Explicit strategy - API endpoints, test runners, architectural patterns
3. **Validation Gates**: Deterministic checks (pytest, ruff, mypy) to catch defects early
4. **Step-by-Step Tasks**: Ordered, atomic tasks with validation commands

**Validation Levels** (execute in order):
1. **Level 1: Syntax & Style** - `ruff check`, `mypy`, `ruff format`
2. **Level 2: Unit Tests** - `uv run pytest` for specific components
3. **Level 3: Integration Tests** - Full system validation
4. **Level 4: Creative/Domain-Specific** - MCP servers, performance testing, security scanning

## Common Commands

### Running PRPs

The primary workflow uses `prp_runner.py` to execute PRPs:

```bash
# Interactive mode (launches Claude Code chat with PRP context)
uv run PRPs/scripts/prp_runner.py --prp <feature-name> --interactive

# Headless mode (non-interactive execution)
uv run PRPs/scripts/prp_runner.py --prp <feature-name>

# With specific PRP file path
uv run PRPs/scripts/prp_runner.py --prp-path PRPs/my-feature.md --interactive

# JSON output formats for automation
uv run PRPs/scripts/prp_runner.py --prp <feature-name> --output-format json
uv run PRPs/scripts/prp_runner.py --prp <feature-name> --output-format stream-json
```

### Slash Commands

The `.claude/` directory contains slash commands organized by workflow:

**PRP Core Workflows:**
- `/prp-core-create <feature-description>` - Create comprehensive feature PRP with deep codebase analysis
- `/prp-core-execute <prp-file>` - Execute a PRP until fully complete
- `/prp-core-review` - Review a PRP for completeness and quality
- `/prp-core-commit` - Commit completed PRP work
- `/prp-core-pr` - Create pull request for PRP changes
- `/prp-core-new-branch` - Create new development branch for PRP work
- `/prp-core-run-all` - Complete end-to-end PRP workflow

**PRP Specialized Types:**
- `/prp-base-create` - Create base PRP using prp_base.md template
- `/prp-spec-create` - Create specification PRP (IndyDevDan style)
- `/prp-planning-create` - Create planning PRP with diagrams
- `/prp-task-create` - Create task-focused PRP
- `/prp-story-create` - Create user story PRP
- `/prp-poc-create-parallel` - Create React POC PRP

**Development:**
- `/onboarding` - Comprehensive codebase analysis for new developers
- `/smart-commit` - Create intelligent git commits
- `/create-pr` - Create pull requests
- `/debug-RCA` - Debug with root cause analysis
- `/new-dev-branch` - Create new development branch

## Development Workflow

### Creating a New Feature

1. **Create PRP**: Use `/prp-core-create` to generate a comprehensive implementation plan
   - Performs deep codebase analysis
   - Gathers external documentation
   - Identifies patterns and integration points
   - Generates step-by-step tasks with validation

2. **Review PRP**: Ensure completeness (context, patterns, validation commands)

3. **Execute PRP**: Use `/prp-core-execute` or run via `prp_runner.py`
   - Execute tasks sequentially
   - Validate after each task
   - Use TodoWrite to track progress
   - Don't proceed if validation fails

4. **Complete**: Move PRP to `PRPs/completed/` when all validation passes

### PRP Runner Integration

`prp_runner.py` wraps PRPs with meta-instructions:
- Planning phase: Think hard, create comprehensive plan with TodoWrite
- Implementation phase: Follow patterns, implement one component at a time
- Testing phase: Test thoroughly, validate against gates
- Completion: Output "DONE" when tests pass, move PRP to completed folder

**Allowed Tools** (when running via prp_runner.py):
- Edit, Bash, Write, MultiEdit, NotebookEdit
- WebFetch, Agent, LS, Grep, Read, NotebookRead
- TodoRead, TodoWrite, WebSearch

## Key Patterns & Anti-Patterns

### Task Format Keywords

Use information-dense keywords:
- **CREATE**: New files or components
- **UPDATE**: Modify existing files
- **ADD**: Insert new functionality
- **REMOVE**: Delete deprecated code
- **REFACTOR**: Restructure without behavior change
- **MIRROR**: Copy pattern from elsewhere
- **READ**: Understand existing patterns
- **FIND**: Search for patterns
- **TEST**: Verify behavior
- **FIX**: Debug and repair
- **VALIDATE**: Execute validation command

### Anti-Patterns to Avoid

❌ Don't create new patterns when existing ones work
❌ Don't skip validation because "it should work"
❌ Don't ignore failing tests - fix them
❌ Don't use sync functions in async context
❌ Don't hardcode values that should be config
❌ Don't catch all exceptions - be specific

### Naming Conventions

From PRP templates:
- **Classes**: CamelCase
- **Functions/variables**: snake_case
- **Files**: snake_case.py or kebab-case.md
- **PRPs**: kebab-case descriptive names

## Context Management

### ai_docs/ Directory

Store library and framework documentation in `PRPs/ai_docs/` for context injection:
- Claude Code specific docs (cc_*.md files present)
- External library documentation
- API references
- Implementation guides

**Available docs**:
- cc_cli.md, cc_mcp.md, cc_hooks.md, cc_settings.md
- cc_commands.md, cc_containers.md, cc_deployment.md
- getting_started.md, hooks.md, subagents.md
- github_actions.md, build_with_claude_code.md

### Context Completeness Check

Before writing PRPs, validate: "If someone knew nothing about this codebase, would they have everything needed to implement successfully?"

Include:
- File paths with line numbers
- Specific patterns to follow (with examples)
- Library documentation URLs with section anchors
- Known gotchas and constraints
- Validation commands that are executable

## PRP Quality Criteria

### Implementation Ready ✓
- Another developer could execute without additional context
- Tasks ordered by dependency (top-to-bottom execution)
- Each task is atomic and independently testable
- Pattern references include specific file:line numbers

### Context Completeness ✓
- All necessary patterns documented
- External library usage with links
- Integration points clearly mapped
- Gotchas and anti-patterns captured
- Every task has executable validation command

### Information Density ✓
- No generic references (all specific and actionable)
- URLs include section anchors
- Task descriptions use codebase keywords
- Validation commands are non-interactive and executable

## Testing & Validation

Always follow the 4-level validation approach:

```bash
# Level 1: Syntax & Style (run after each file)
ruff check src/{new_files} --fix
mypy src/{new_files}
ruff format src/{new_files}

# Level 2: Unit Tests (test each component as created)
uv run pytest src/services/tests/test_{domain}_service.py -v
uv run pytest src/tools/tests/test_{action}_{resource}.py -v

# Level 3: Integration (full system validation)
uv run python main.py &
curl -f http://localhost:8000/health

# Level 4: Creative validation (MCP servers, performance, security)
# Project-specific domain validation commands
```

## Important Notes

- **TodoWrite Usage**: Always use TodoWrite to track progress through PRP tasks
- **Sequential Execution**: Execute PRP tasks in order, validate each before proceeding
- **Trust but Verify**: Trust PRP strategy, but verify tactical details (imports, paths, names)
- **Fix and Note**: If PRP has detail errors, fix them and note in completion report
- **Completion Criteria**: Move PRP to completed/ only when ALL validation passes
- **No Shortcuts**: Never skip validation because "it should work"
