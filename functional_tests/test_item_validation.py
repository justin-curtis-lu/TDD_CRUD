import pytest

def test_cannot_add_empty_list_items(context, live_server):
    # context.tracing.start(screenshots=True, snapshots=True)
    p = context.new_page()
    p.set_default_timeout(3000)
    p.goto(live_server.url)

    new_item_input = p.locator("id=id_text")

    # attempt to enter nothing and submit a list, generating an error
    new_item_input.fill("")
    new_item_input.press("Enter")
    # print(p.locator(":invalid").first.screenshot())
    # p.locator(":invalid").first.screenshot(path="error-screenshot.png")
    # HTML is being escaped here
    # empty_list_error_text = p.inner_text(".has-error")
    # assert empty_list_error_text == "You can't have an empty list item"

    # user correctly enters an item in the list
    new_item_input.fill("Buy Milk")
    new_item_input.press("Enter")
    # table_text = p.locator("id=id_list_table").inner_text()
    # assert "1: Buy Milk" in table_text

    # user tries to enter a second blank item
    new_item_input.fill("")
    new_item_input.press("Enter")
    # empty_list_error_text = p.inner_text(".has-error")
    # assert empty_list_error_text == "You can't have an empty list item"

    # and corrects it by adding a second item
    new_item_input.fill("Make Tea")
    new_item_input.press("Enter")

    table_text = p.locator("id=id_list_table").inner_text()

    # p.context.tracing.stop(path="trace.zip")

    assert "1: Buy Milk" in table_text
    assert "2: Make Tea" in table_text


# @pytest.mark.skip
def test_cannot_add_duplicate_items(context, live_server):
    p = context.new_page()
    p.set_default_timeout(3000)
    p.goto(live_server.url)

    new_item_input = p.locator("id=id_text")
    new_item_input.fill("Buy wellies")
    new_item_input.press("Enter")

    table_text = p.locator("id=id_list_table").inner_text()
    assert "Buy wellies" in table_text

    new_item_input.fill("Buy wellies")
    new_item_input.press("Enter")

    error_text = p.inner_text(".has-error")
    assert "You've already got this in your list" in error_text