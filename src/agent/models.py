from pydantic import BaseModel
from typing import List

# Simple DTOs (Data Transfer Objects) to enforce structure on our scraped data.
# This ensures we don't pass random dicts around the app.

class PageLink(BaseModel):
    text: str
    href: str

class PageSummary(BaseModel):
    title: str
    headings: List[str]
    # Nesting the list of objects guarantees validation for every single link
    links: List[PageLink]