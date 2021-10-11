from pytest_django.asserts import assertTemplateUsed, assertContains, assertNotContains, assertRedirects
from django.core.exceptions import ValidationError
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
import pytest

from lists.views import home_page
from lists.models import Item, List

# List & Model Test Cases
@pytest.mark.django_db
def test_saving_and_retrieving_items(client):
    list_ = List()
    list_.save()

    first_item = Item()
    first_item.text = 'The first (ever) list item'
    first_item.list = list_
    first_item.save()

    second_item = Item()
    second_item.text = 'Item the second'
    second_item.list = list_
    second_item.save()

    saved_list = List.objects.first()
    assert saved_list == list_


    saved_items = Item.objects.all()
    assert saved_items.count() == 2

    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    assert first_saved_item.text == 'The first (ever) list item'
    assert first_saved_item.list == list_
    assert second_saved_item.text == 'Item the second'
    assert second_saved_item.list == list_


@pytest.mark.django_db
def test_cannot_save_empty_list_items(client):
    list_ = List.objects.create()
    item = Item(list=list_, text='')
    with pytest.raises(ValidationError):
        item.save()
        item.full_clean()


@pytest.mark.django_db
def test_get_absolute_url(client):
    list_ = List.objects.create()
    assert list_.get_absolute_url() == f'/lists/{list_.id}/'


@pytest.mark.django_db
def test_duplicate_items_are_invalid(client):
    list_ = List.objects.create()
    Item.objects.create(list=list_, text='bla')
    with pytest.raises(ValidationError):
        item = Item(list=list_, text='bla')
        item.full_clean()


@pytest.mark.django_db
def test_CAN_save_same_item_to_different_lists(client):
    list1 = List.objects.create()
    list2 = List.objects.create()
    Item.objects.create(list=list1, text='bla')
    item = Item(list=list2, text='bla')
    item.full_clean()


@pytest.mark.django_db
def test_list_ordering(client):
    list1 = List.objects.create()
    item1 = Item.objects.create(list=list1, text='i1')
    item2 = Item.objects.create(list=list1, text='item 2')
    item3 = Item.objects.create(list=list1, text='3')
    assert list(Item.objects.all()) == [item1, item2, item3]


@pytest.mark.django_db
def test_string_representation(client):
    item = Item(text='some text')
    assert str(item) == 'some text'
