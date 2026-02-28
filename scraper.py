import asyncio
import re
from playwright.async_api import async_playwright

BASE_URL = "https://exam.sanand.workers.dev/tds-2026-01-ga3?seed={}"
SEEDS = range(14, 24)

async def extract_sum(page, url):
    await page.goto(url, timeout=60000)
    await page.wait_for_load_state("networkidle")

    text = await page.evaluate("document.body.innerText")

    numbers = re.findall(r'-?\d+(?:\.\d+)?', text)
    numbers = [float(n) for n in numbers]

    return sum(numbers)

async def main():
    grand_total = 0

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for seed in SEEDS:
            url = BASE_URL.format(seed)
            print(f"Visiting {url}")
            page_sum = await extract_sum(page, url)
            print(f"Seed {seed} sum = {page_sum}")
            grand_total += page_sum

        await browser.close()

    print(int(grand_total))   # ← ONLY number for grader

asyncio.run(main())
