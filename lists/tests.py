from pytest_django.asserts import assertTemplateUsed, assertContains, assertNotContains, assertRedirects
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
import pytest

from lists.views import home_page
from lists.models import Item


# Home Test Cases
@pytest.mark.django_db
def test_home_page_html(client):
    response = client.get('/')
    html = response.content.decode('utf8')

    assert html.startswith('<html>')
    assert '<title>To-Do lists</title>' in html
    assert html.strip().endswith('</html>')

    assertTemplateUsed(response, 'home.html')


@pytest.mark.django_db
def test_can_save_a_post_request(client):
    response = client.post('/', data={'item_text': 'A new list item'})

    assert Item.objects.count() == 1
    new_item = Item.objects.first()
    assert new_item.text == 'A new list item'


@pytest.mark.django_db
def test_redirects_after_post(client):
    response = client.post('/', data={'item_text': 'A new list item'})

    assert response.status_code == 302
    assert response['location'] == '/'


@pytest.mark.django_db
def test_only_saves_items_when_necessary(client):
    response = client.get('/')
    assert Item.objects.count() == 0


@pytest.mark.django_db
def test_displays_all_list_items(client):
    Item.objects.create(text='test 1')
    Item.objects.create(text='test 2')

    response = client.get('/')

    assertContains(response, 'test 1')
    assertContains(response, 'test 2')


# Model Test Cases
@pytest.mark.django_db
def test_saving_and_retrieving_items(client):
    first_item = Item()
    first_item.text = 'The first (ever) list item'
    first_item.save()

    second_item = Item()
    second_item.text = 'Item the second'
    second_item.save()

    saved_items = Item.objects.all()
    assert saved_items.count() == 2

    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    assert first_saved_item.text == 'The first (ever) list item'
    assert second_saved_item.text == 'Item the second'
