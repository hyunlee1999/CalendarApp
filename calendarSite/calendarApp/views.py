from django.shortcuts import render
from django.http import HttpResponse
from .models import Group, TodoList, TodoItem

def index(request):
    num_Groups = Group.objects.all().count()
    num_TodoList = TodoList.objects.all().count()
    num_TodoItem = TodoItem.objects.all().count()

    context = {
        "num_Groups": num_Groups,
        "num_TodoList": num_TodoList,
        "num_TodoItem": num_TodoItem,
    }

    return render(request, "index.html", context=context)
