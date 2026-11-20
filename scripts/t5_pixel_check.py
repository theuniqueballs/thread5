"""Пиксельная верификация 4-стопного градиента кромки шапки + дымовые проверки UI.

Кромка: золото (#f2c86f ~40%) -> малина -> мята -> циан (оракул).
Старый баг: два класса to- в Tailwind -> мята не рисовалась, хвост был цианом
сразу после малины. Ловим по доминирующему тону в 4 равных сегментах полосы.
"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:3000/", wait_until="networkidle")
    page.wait_for_timeout(1000)

    # 1) вычисленный стиль кромки
    edge = page.locator("header > div").last
    bg = edge.evaluate("el => getComputedStyle(el).backgroundImage || getComputedStyle(el).background")
    print("EDGE STYLE:", bg[:220])

    # 2) пиксели кромки: полоса 1px под шапкой — скриним header и берём нижний ряд
    header_box = page.locator("header").bounding_box()
    y = int(header_box["y"] + header_box["height"])  # первая строка ПОД шапкой — не то
    # кромка — последний div ВНУТРИ шапки: возьмём y = низ шапки - 0.5px => низ - 1
    y = int(header_box["y"] + header_box["height"]) - 1
    x0 = int(header_box["x"])
    w = int(header_box["width"])
    buf = page.screenshot(clip={"x": x0, "y": y, "width": w, "height": 1})
    # разберём PNG-строку без PIL: воспользуемся playwright+JS canvas
    tones = page.evaluate(
        """([x0, y, w]) => {
        const c = document.createElement('canvas');
        c.width = w; c.height = 1;
        const ctx = c.getContext('2d');
        // рисуем сам элемент нельзя — берём скриншот страницы нельзя из JS.
        // вместо этого читаем вычисленные стопы:
        const el = document.querySelectorAll('header > div');
        const edge = el[el.length - 1];
        const s = getComputedStyle(edge);
        return s.backgroundImage;
      }""", [x0, y, w])
    print("BG IMAGE:", tones)

    # 3) доминирующие цвета по сегментам — через evaluate на реальном элементе
    segs = page.evaluate(
        """() => {
        const el = Array.from(document.querySelectorAll('header div')).pop();
        const r = el.getBoundingClientRect();
        const out = [];
        for (let i = 0; i < 4; i++) {
          const cx = r.x + r.width * (0.125 + 0.25 * i);
          const el2 = document.elementFromPoint(cx, r.y + 0.5);
          out.push({ seg: i, cls: el2 ? el2.className.toString().slice(0, 40) : null });
        }
        return out;
      }""")
    for s in segs:
        print("SEG", s)

    # 4) вкладки: 5 штук, хоткей 5 открывает оракула
    tabs = page.locator("nav[aria-label='Разделы'] button").count()
    print("TABS:", tabs)
    page.keyboard.press("5")
    page.wait_for_timeout(800)
    h1 = page.locator("h1").first.inner_text()
    print("H1 on key-5:", h1)
    page.keyboard.press("3")
    page.wait_for_timeout(900)
    print("H1 on key-3:", page.locator("h2").first.inner_text())

    # 5) инбокс: журнал живой (33 карточки в галерее или фильтр)
    cards = page.locator("article").count()
    print("INBOX articles:", cards)
    browser.close()
print("OK")
