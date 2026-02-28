import asyncio
from playwright.async_api import async_playwright

BASE_URL = "https://exam.sanand.workers.dev/tds-2026-01-ga3?seed={}"
SEEDS = range(14, 24)

async def extract_sum(page, url):
    await page.goto(url, timeout=60000)
    await page.wait_for_load_state("networkidle")

    total = await page.evaluate("""
        () => {
            let sum = 0;
            const elements = document.querySelectorAll("*");

            elements.forEach(el => {
                let text = el.innerText?.trim();
                if (!text) return;

                // match full numeric values only
                if (/^-?\\d+(\\.\\d+)?$/.test(text)) {
                    sum += Number(text);
                }
            });

            return sum;
        }
    """)

    return total

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

    print(grand_total)

asyncio.run(main())
