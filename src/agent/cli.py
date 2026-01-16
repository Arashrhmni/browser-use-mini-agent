import argparse
import asyncio
import json
from .browser import fetch_page_source
from .extract import extract_page_data
import os
from .config import load_config

load_config()
# Fail fast if the key is missing—no point starting the browser without it.
if not os.getenv("BROWSER_USE_API_KEY"):
    raise SystemExit("BROWSER_USE_API_KEY is not set. Put it in .env or export it.")


def main():
    # Simple CLI setup.
    parser = argparse.ArgumentParser(description="Browser-Use Mini Agent")
    parser.add_argument("command", choices=["scrape"], help="Command to run")
    parser.add_argument("--url", required=True, help="URL to scrape")
    parser.add_argument("--out", required=True, help="Output JSON file path")
    
    args = parser.parse_args()
    
    if args.command == "scrape":
        print(f"🚀 Visiting {args.url}...")
        
        # 1. Hit the site. We need asyncio.run wrapper since main() is synchronous.
        html = asyncio.run(fetch_page_source(args.url))
        
        # 2. Pass the raw HTML to our extraction logic (LLM or parser).
        print("🔍 Extracting data...")
        data = extract_page_data(html)
        
        # 3. Dump the Pydantic model straight to JSON.
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(data.model_dump_json(indent=2))
            
        print(f"✅ Done! Saved to {args.out}")

if __name__ == "__main__":
    main()