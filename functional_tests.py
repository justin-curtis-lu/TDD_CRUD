from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.firefox.launch()
    page = browser.new_page()
    page.goto('http://localhost:8000')
    assert 'Django' in page.title()
    browser.close()