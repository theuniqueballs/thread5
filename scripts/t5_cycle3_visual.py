"""Визуальная проверка цикла 3 «двойной аудит»: прилавок, оракул-панель
(режимы оценки P1-05), инбокс. Скриншоты в /tmp/render/."""
from playwright.sync_api import sync_playwright

OUT = "/tmp/render"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 960})
    page.goto("http://localhost:3000/", wait_until="networkidle")
    page.wait_for_timeout(1500)
    page.screenshot(path=f"{OUT}/c3-01-batches.png")
    # вкладка оракула (клавиша 5)
    page.keyboard.press("5")
    page.wait_for_timeout(1500)
    page.screenshot(path=f"{OUT}/c3-02-oracle.png", full_page=False)
    # скролл к экспресс-оценке
    page.evaluate("document.querySelector('textarea')?.scrollIntoView({block:'center'})")
    page.wait_for_timeout(400)
    # ввод текста и оценка — проверяем блок РЕЖИМ: LOCAL-LITE
    ta = page.locator("textarea").first
    ta.fill("upper body frontal, 1girl, solo, the towel is the claim, hands pressed over her chest, onsen steam, wet skin, collarbone highlight")
    page.wait_for_timeout(200)
    ta.press("Control+Enter")
    page.wait_for_timeout(2500)
    page.evaluate("document.querySelector('textarea')?.scrollIntoView({block:'center'})")
    page.wait_for_timeout(400)
    page.screenshot(path=f"{OUT}/c3-03-rate-mode.png")
    # инбокс
    page.keyboard.press("3")
    page.wait_for_timeout(1200)
    page.screenshot(path=f"{OUT}/c3-04-inbox.png")
    browser.close()
print("скриншоты готовы")
