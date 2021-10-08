from pytest_django.asserts import assertTemplateUsed, assertContains, assertNotContains, assertRedirects
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
import pytest

from lists.views import home_page


def test_home_page_html(client):
    response = client.get('/')
    html = response.content.decode('utf8')

    assert html.startswith('<html>')
    assert '<title>To-Do lists</title>' in html
    assert html.strip().endswith('</html>')

    assertTemplateUsed(response, 'home.html')
