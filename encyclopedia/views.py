"""views for app encyclopedia"""
import random
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import markdown
from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "enteries": util.list_entries(),
        "title": "All Pages"
    })

def entry(request,title):
    content=util.get_entry(title)
    markdowner= markdown.Markdown()
    if content is not None:
        title_content=markdowner.convert(content)
        return render (request,"encyclopedia/entry.html",{
            "title": title,
            "content": title_content
        })
    else:
        return render (request, "encyclopedia/error.html",{
            "error_message":"This entry does not exist"
        })

def search(request):
    recommend = []
    if request.method == "POST":
        title_search = request.POST['q']
        exist_title = util.get_entry(title_search)
        if exist_title is not None:
            return HttpResponseRedirect(reverse("entry", kwargs={'title': title_search}))
        else:
            titles=util.list_entries()
            for enteries in titles:
                if title_search.upper() in enteries.upper():
                    recommend.append(enteries)
            if recommend is not None:
                return render (request,"encyclopedia/index.html",{
                "enteries": recommend,
                "title":"Recommended Pages"
                })
            else:
                return render (request, "encyclopedia/error.html",{
                "error_message":"This entry does not exist"
                })

def new_page(request):
    if request.method=="GET":
        return render (request, "encyclopedia/new_page.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        exist_title = util.get_entry(title)
        if exist_title is not None:
            return render (request, "encyclopedia/error.html",{
                "error_message":"This page already exists."
            })
        elif title == "":
            return render (request, "encyclopedia/error.html",{
            "error_message":"Please Enter Information to Create Page"
            })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))

def edit(request,title):
    if request.method=="POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
    entry_content = util.get_entry(title)
    return render (request,"encyclopedia/edit_page.html",{
    "title": title,
    "content": entry_content
    })

def ran_page(request):
    titles=util.list_entries()
    ran_title = random.choice(titles)
    return HttpResponseRedirect(reverse("entry", kwargs={'title': ran_title}))
