from bs4 import BeautifulSoup
from .models import PageSummary, PageLink

def extract_page_data(html_content: str) -> PageSummary:
    # Using 'html.parser' because it's built-in. Use 'lxml' if this gets too slow later.
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 1. Grab title safely (some raw HTML fragments might actually miss a <title> tag).
    title = soup.title.string if soup.title else "No Title"
    
    # 2. Extract main headers to get the gist of the content structure.
    # strip=True cleans up the newlines/tabs inside tags.
    headings = [
        h.get_text(strip=True)
        for h in soup.find_all(["h1", "h2", "h3"])
    ]
    
    # 3. Get links, but cap at 5. 
    # Otherwise, we risk flooding the output with footer/nav links.
    links = []
    for a in soup.find_all("a", href=True)[:5]:
        links.append(
            PageLink(
                text=a.get_text(strip=True),
                href=a["href"]
            )
        )
    # Wrap it all up in our Pydantic model for clean downstream usage.    
    return PageSummary(
        title=title,
        headings=headings,
        links=links
    )