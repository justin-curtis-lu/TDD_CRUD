import playwright.sync_api
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import os
# from dotenv import load_dotenv

# load_dotenv()
# GALAXY_AUTH = os.getenv('STAGING_SERVER')

def test_multiple_users_can_start_lists_at_different_urls(context, live_server):
    staging_server = os.environ.get('STAGING_SERVER')
    if staging_server:
        live_server.url = 'http://' + staging_server
    p = context.new_page()
    p.set_default_timeout(3000)
    p.goto(live_server.url)

    new_item_input = p.locator("id=id_new_item")
    new_item_input.fill("Buy peacock feathers")
    new_item_input.press("Enter")

    text = p.locator("id=id_list_table").inner_text()
    assert text == "1: Buy peacock feathers"

    url1 = p.url
    p.close()

    # open a new p, try again
    p = context.new_page()
    p.goto(live_server.url)

    # the new list doesn't have old text upon opening
    text = p.inner_text("body")
    assert "1: Buy peacock feathers" not in text

    new_item_input = p.locator("id=id_new_item")
    new_item_input.fill("Buy Milk")
    new_item_input.press("Enter")
    text = p.locator("id=id_list_table").inner_text()
    assert "1: Buy Milk" in text

    url2 = p.url

    assert url1 != url2
