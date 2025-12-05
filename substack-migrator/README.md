# Substack Migrator

Migrate Substack posts to Jekyll format with proper front matter and downloaded images.

## Setup

```bash
cd substack-migrator
uv sync
```

## Usage

```bash
uv run migrate.py https://alexandrevariengien.substack.com/p/your-post-slug
```

### Options

| Flag | Description |
|------|-------------|
| `--permalink` | Override the generated permalink |
| `--date` | Override the date (YYYY-MM-DD) |
| `--output-dir` | Custom output directory (default: `../_posts`) |
| `--assets-dir` | Custom assets directory (default: `../assets`) |

### Example

```bash
uv run migrate.py "https://alexandrevariengien.substack.com/p/sea-snails-in-a-cocaine-vaccine" \
  --date 2025-11-25 \
  --permalink sea-snails-cocaine-vaccine
```

## What it does

- Extracts title, subtitle, and content from Substack posts
- Converts HTML to markdown with preserved links
- Downloads images to `assets/img/{slug}/`
- Generates proper Jekyll front matter
- Filters out Substack boilerplate (subscribe buttons, etc.)

