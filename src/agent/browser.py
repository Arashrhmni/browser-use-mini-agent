import json
from browser_use import Agent, Browser, ChatBrowserUse
from .models import PageSummary, PageLink


async def agent_extract_page(url: str) -> PageSummary:
    """
    Agent-driven browser navigation + in-browser JS extraction.
    For Hacker News, this extracts the top story links (span.titleline > a).
    """
    browser = Browser(
        use_cloud=True,
        keep_alive=True,
        enable_default_extensions=False,
    )

    await browser.start()
    try:
        llm = ChatBrowserUse()

        agent = Agent(
            task=f"Open {url} and wait until the page is fully loaded.",
            browser_session=browser,
            llm=llm,
        )

        await agent.run()

        page = await browser.get_current_page()
        if page is None:
            await browser.new_page(url)
            page = await browser.get_current_page()

        # Extract data inside the browser. We return a JSON string on purpose
        # to avoid "dict vs string" inconsistencies across runtimes.
        raw = await page.evaluate(
            """() => JSON.stringify({
              title: document.title || "No Title",
              headings: Array.from(document.querySelectorAll("h1,h2,h3"))
                .map(h => (h.innerText || "").trim())
                .filter(Boolean),

              // Hacker News top story title links
              links: Array.from(document.querySelectorAll("span.titleline > a"))
                .slice(0, 5)
                .map(a => ({
                  text: (a.textContent || "").trim(),
                  href: a.href
                })),
            })"""
        )

        data = json.loads(raw)

        return PageSummary(
            title=data["title"],
            headings=data["headings"],
            links=[PageLink(**l) for l in data["links"]],
        )

    finally:
        await browser.kill()
