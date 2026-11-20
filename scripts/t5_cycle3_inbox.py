from playwright.sync_api import sync_playwright

OUT = "/tmp/render"
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 960})
    page.goto("http://localhost:3000/", wait_until="networkidle")
    page.wait_for_timeout(1200)
    # клик по вкладке «Инбокс» в навигации (не хоткей — фокус мог остаться в поле)
    page.get_by_text("Инбокс", exact=True).first.click()
    page.wait_for_timeout(2000)
    page.screenshot(path=f"{OUT}/c3-04-inbox.png")
    browser.close()
print("инбокс переснят")
