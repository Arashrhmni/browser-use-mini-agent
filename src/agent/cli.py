import argparse
import asyncio
from .browser import agent_extract_page
import os
from .config import load_config

load_config()
# Fail fast if the key is missing—no point starting the browser without it.
if not os.getenv("BROWSER_USE_API_KEY"):
    raise SystemExit("BROWSER_USE_API_KEY is not set. Put it in .env or export it.")

def main():
    parser = argparse.ArgumentParser(description="Browser-Use Mini Agent")
    parser.add_argument("command", choices=["scrape"])
    parser.add_argument("--url", required=True)
    parser.add_argument("--out", required=True)

    args = parser.parse_args()

    if args.command == "scrape":
        print(f"🚀 Visiting {args.url}...")

        data = asyncio.run(agent_extract_page(args.url))

        with open(args.out, "w", encoding="utf-8") as f:
            f.write(data.model_dump_json(indent=2))

        print(f"✅ Done! Saved to {args.out}")

if __name__ == "__main__":
    main()