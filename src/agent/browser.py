from browser_use import Agent, Browser, ChatBrowserUse

async def fetch_page_source(url: str) -> str:
    # Set keep_alive=True so we can still access the HTML after the agent is done.
    # Also disabling extensions to skip the SSL/manifest warnings.
    browser = Browser(keep_alive=True, enable_default_extensions=False)

    await browser.start()
    try:
        llm = ChatBrowserUse()

        # Pass our specific browser instance here so the agent reuses the session
        # instead of spinning up a totally new window.
        agent = Agent(
            task=f"Open {url} and wait until the page is fully loaded.",
            browser_session=browser,
            llm=llm,
        )

        # Run the agent
        await agent.run()

        # The browser should still be connected here since we flagged it to stay alive.
        page = await browser.get_current_page()
        if page is None:
            # Handle the edge case where the page context gets lost: just re-open in the current session.
            await browser.new_page(url)
            page = await browser.get_current_page()

        html = await page.evaluate("() => document.documentElement.outerHTML")
        return html

    finally:
        # Important: standard stop() won't actually close the window when keep_alive is on.
        # kill() forces a proper shutdown so we don't leave zombie processes.
        await browser.kill()
