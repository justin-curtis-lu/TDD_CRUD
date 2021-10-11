from django.shortcuts import redirect, render
from lists.forms import ItemForm
from lists.models import Item, List
from django.core.exceptions import ValidationError


def home_page(request):
    # Home Page passes blank item form which is used to collect proper data
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    # On list html, when the form is POST
    # Similar to new list however all we do is grab an existing list not a new list
    # And add the item to it
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        # Valid item form, save data to associated list
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})


def new_list(request):
    # On home html, when the form is POST
    # Routes to this URL, which takes the form and fills in the data
    # Build a new list and save the item
    form = ItemForm(data=request.POST)
    # Valid means non empty
    if form.is_valid():
        # Successful item form
        # Thus save this form data to the associated list (new in this case)
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})
