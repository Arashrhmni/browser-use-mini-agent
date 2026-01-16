from pathlib import Path
from src.agent.extract import extract_page_data

def test_extract_page_data():
    # Load a static HTML fixture so we don't need network access for unit tests.
    # This keeps the test fast and deterministic.
    html = Path("tests/fixtures/sample.html").read_text(encoding="utf-8")
    data = extract_page_data(html)

    # Sanity checks on the extracted fields
    assert data.title == "Sample Page"
    # Check that our heading parser captures both h1 and h2/h3 logic correctly
    assert "Main Heading" in data.headings
    assert "Sub Heading" in data.headings
    # We expect at least a couple of links from the sample file.
    # Checking the first one specifically to ensure the object structure (text + href) is valid.
    assert len(data.links) >= 2
    assert data.links[0].text == "Example"
    assert data.links[0].href == "https://example.com"