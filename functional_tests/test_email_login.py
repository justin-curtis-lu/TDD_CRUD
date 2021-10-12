from django.core import mail
from accounts.models import User
import playwright.sync_api
import re
import pytest

TEST_EMAIL = 'test123@gmail.com'
SUBJECT = 'Your login link for Superlists'

# @pytest.mark.skip
def test_can_recieve_email_link(context, live_server):
    p = context.new_page()
    p.set_default_timeout(3000)
    p.goto(live_server.url)

    email_input = p.locator('input').first
    email_input.fill(TEST_EMAIL)
    email_input.press("Enter")

    assert 'Check your email' in p.text_content('body')

    email = mail.outbox[0]
    assert TEST_EMAIL in email.to
    assert email.subject == SUBJECT

    assert 'Use this link to log in:' in email.body
    url_search = re.search(r'http://.+/.+$', email.body)
    if not url_search:
        pytest.fail("Could not find the url in email body: " + email.body)

    url = url_search.group(0)
    assert live_server.url in url
    p.goto(url)

    navbar = p.locator(".navbar")
    assert "Log out" in p.locator('text=Log out').inner_text()
    assert TEST_EMAIL in navbar.inner_text()

    p.click('text=Log out')
    print(navbar.inner_text())
    assert TEST_EMAIL not in navbar.inner_text()