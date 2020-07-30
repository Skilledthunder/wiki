from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
import markdown2
import random



from . import util

class SearchForm(forms.Form):
    term = forms.CharField(required=False)

def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            search = data.get("search")
            item_list = util.list_entries()
            possible_list = []
            for item in item_list:
                if item.lower() == search.lower():
                    return redirect(f"wiki/{item}")
            length = len(search)
            for item in item_list:
                if search.lower() == item[0:length].lower():
                    possible_list.append(item)
            if possible_list:
                return render(request, "encyclopedia/index.html", {
                    "entries": possible_list,
                    })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry(request, item_name):
    items = util.list_entries()
    for item in items:
        if item_name == item:
            html = markdown2.markdown_path(fr".\entries\{item}.md")
            item = util.get_entry(item)
            return render(request, "encyclopedia/entry.html", {
                "html": html,
                "item": item_name,
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def new_page(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            title = data.get("title")
            text = data.get("new_data")
            item_list = util.list_entries()
            for item in item_list:
                if item.lower() == title.lower():
                    messages.error(request, 'ERROR: Title Already Exists.')
                    return render(request,"encyclopedia/new_page.html")
            util.save_entry(title, text)
            print("Entry saved")
            return redirect(f"wiki/{title}")
    else:
        return render(request, "encyclopedia/new_page.html")

def rand(request):
    item_list = util.list_entries()
    amount = len(item_list)
    #Note: look into better way to implement this
    number = round(random.uniform(0, amount - 1))
    print(number)
    items = []
    for item in item_list:
        items.append(item)
    return redirect((f"wiki/{items[number]}"))

def edit(request, item):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            data = request.POST.copy()
            title = data.get("title")
            text = data.get("new_data")
            util.save_entry(title, text)
            print("Entry saved")
            return redirect(f"../wiki/{title}")
    item_list = util.list_entries()
    for entry in item_list:
        if item == entry:
            content = util.get_entry(item)
            return render(request, "encyclopedia/edit.html", {
                "item": item,
                "content": content
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })
        