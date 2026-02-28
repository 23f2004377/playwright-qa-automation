import asyncio
from playwright.async_api import async_playwright

BASE_URL = "PBASE_URL = "https://exam.sanand.workers.dev/tds-2026-01-ga3?seed={}"

SEEDS = range(14, 24)

async def extract_sum(page, url):
    await page.goto(url)
    await page.wait_for_selector("table")

    total = await page.evaluate("""
        () => {
            let sum = 0;
            document.querySelectorAll("td").forEach(cell => {
                let text = cell.innerText.trim().replace(/,/g, "");
                let num = Number(text);
                if (!isNaN(num)) sum += num;
            });
            return sum;
        }
    """)
    return total

async def main():
    grand_total = 0

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        for seed in SEEDS:
            url = BASE_URL.format(seed)
            page_sum = await extract_sum(page, url)
            print(f"Seed {seed} sum = {page_sum}")
            grand_total += page_sum

        await browser.close()

    print("FINAL TOTAL =", grand_total)

asyncio.run(main())
