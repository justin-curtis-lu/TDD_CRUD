import django
import pytest
from lists.models import Item, List
from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm
)

from lists.forms import EMPTY_ITEM_ERROR, ItemForm
from lists.models import Item, List


@pytest.mark.django_db
def test_form_item_input_has_placeholder_and_css_classes(client):
    # Testing that the item form is rendering our desired CSS
    form = ItemForm()
    assert 'placeholder="Enter a to-do item"' in form.as_p()
    assert 'class="form-control input-lg"' in form.as_p()


@pytest.mark.django_db
def test_form_validation_for_blank_items(client):
    # Ensures we can not send empty data on the form side
    form = ItemForm(data={'text': ''})
    assert form.is_valid() == False
    assert form.errors['text'] == [EMPTY_ITEM_ERROR]


@pytest.mark.django_db
def test_form_save_handles_saving_to_a_list(client):
    # Ensures that when we fill out an item form
    # we can properly save the data to a list
    list_ = List.objects.create()
    form = ItemForm(data={'text': 'do me'})
    new_item = form.save(for_list=list_)
    assert new_item == Item.objects.first()
    assert new_item.text == 'do me'
    assert new_item.list == list_


# Existing List Test Cases
@pytest.mark.django_db
def test_existing_item_form_renders_text_input():
    l = List.objects.create()
    form = ExistingListItemForm(for_list=l)
    assert 'placeholder="Enter a to-do item"' in form.as_p()

@pytest.mark.django_db
def test_existing_item_form_validation_for_blank_items():
    l = List.objects.create()
    form = ExistingListItemForm(for_list=l,data={'text':''})
    assert form.is_valid() == False
    assert form.errors['text'] == [EMPTY_ITEM_ERROR]


@pytest.mark.django_db
def test_existing_item_form_validation_for_duplicate_items():
    l = List.objects.create()
    Item.objects.create(list=l, text='no duplicates')
    form = ExistingListItemForm(for_list=l,data={'text':'no duplicates'})
    assert form.is_valid() == False
    assert form.errors['text'] == [DUPLICATE_ITEM_ERROR]


@pytest.mark.django_db
def test_form_save(client):
    list_ = List.objects.create()
    form = ExistingListItemForm(for_list=list_, data={'text': 'hi'})
    new_item = form.save()
    assert new_item == Item.objects.all()[0]
