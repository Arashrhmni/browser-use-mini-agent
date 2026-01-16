# browser-use-mini-agent

A small, professional Python CLI that demonstrates agent-based browser automation using browser-use.
The tool opens a URL with a browser agent, extracts simple but useful page information, and saves the result as JSON.

This repository is intentionally minimal and structured to reflect a realistic interview-level use case for
Browser-Use–based agent workflows.

---

## What it does

Given a URL, the CLI tool:

1. Uses a browser-use Agent to open and navigate to the page
2. Waits until the page is fully loaded
3. Extracts:
   - Page title
   - Headings (h1–h3)
   - A small set of links (text + href)
4. Saves the extracted data to a JSON file

---

## Quickstart

### 1) Install dependencies

This project uses uv for dependency management.

```bash
uv sync
```

---

### 2) Configure environment

Create a `.env` file in the repository root:

```bash
BROWSER_USE_API_KEY=your_api_key_here
```

Note:
Tests do NOT require a browser or API key.
The API key is only required when running the CLI scrape command.

---

### 3) Run the CLI

```bash
uv run -m src.agent.cli scrape --url "https://news.ycombinator.com" --out result.json
```

After completion, the extracted data will be saved to `result.json`.

---

## Example output

```json
{
  "title": "Hacker News",
  "headings": [],
  "links": [
    {
      "text": "new",
      "href": "news"
    },
    {
      "text": "past",
      "href": "front"
    }
  ]
}
```

---

## Project structure

```text
browser-use-mini-agent/
├─ src/agent/
│  ├─ __init__.py
│  ├─ cli.py          # CLI entrypoint
│  ├─ browser.py      # Browser-Use / agent logic
│  ├─ extract.py      # Pure HTML → data extraction
│  └─ models.py       # Pydantic output models
├─ tests/
│  ├─ test_extract.py
│  └─ fixtures/
│     └─ sample.html
├─ examples/
│  └─ example_output.json
├─ .github/workflows/ci.yml
├─ pyproject.toml
└─ README.md
```

---

## Design decisions

- Agent-first approach: page navigation is handled by a Browser-Use agent, not direct HTTP requests
- Separation of concerns: browser automation and HTML parsing are strictly separated
- Testability: extraction logic is pure and tested using static HTML fixtures

---

## Limitations

- Browser automation can be flaky depending on network conditions and rendering timing
- Extraction logic is intentionally generic and does not handle complex client-side frameworks
- This is a minimal demo, not a full crawler or production scraper

---

## Why this project

This repository demonstrates:
- Agent-based workflows with Browser-Use
- Clean Python project structure
- Testable extraction logic
- A realistic, interview-ready CLI use case