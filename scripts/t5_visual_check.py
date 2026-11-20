"""Визуальная проверка прилавка THREAD 5 после инженерного цикла 2.

Скриншоты: прилавок (кромка шапки — 4-стопный градиент), инбокс, оракул.
Сохраняются в /tmp/render/t5-*.png.
"""
from playwright.sync_api import sync_playwright

OUT = "/tmp/render"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:3000/", wait_until="networkidle")
    page.wait_for_timeout(1200)
    page.screenshot(path=f"{OUT}/t5-01-batches.png")
    # кромка шапки крупно (золото -> малина -> мята -> циан)
    header = page.locator("header")
    header.screenshot(path=f"{OUT}/t5-02-header.png")
    # инбокс
    page.keyboard.press("3")
    page.wait_for_timeout(1500)
    page.screenshot(path=f"{OUT}/t5-03-inbox.png")
    # оракул
    page.keyboard.press("5")
    page.wait_for_timeout(2000)
    page.screenshot(path=f"{OUT}/t5-04-oracle.png")
    browser.close()
print("done")
