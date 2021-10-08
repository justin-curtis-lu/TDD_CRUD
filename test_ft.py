from playwright.sync_api import Page
import pytest

def test_new_visitor(page):
    page.goto("http://localhost:8000")
    page.set_default_timeout(3000)
    assert 'To-Do' in page.title()
    placeholder = page.get_attribute("id=id_new_item", "placeholder")
    assert placeholder == "Enter a to-do item"
    new_item_input = page.locator("id=id_new_item")
    new_item_input.fill("Buy peacock feathers")
    new_item_input.press("Enter")
    text = page.locator("id=id_list_table").inner_text()
    assert text == "1: Buy peacock feathers"

    new_item_input = page.locator("id=id_new_item")
    new_item_input.fill("Use peacock feathers to make a fly")
    new_item_input.press("Enter")
    text = page.locator("id=id_list_table").inner_text()
    assert "2: Use peacock feathers to make a fly" in text

