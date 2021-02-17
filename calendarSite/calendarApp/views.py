from django.shortcuts import render
from django.http import HttpResponse
from .models import Group, TodoList, TodoItem
from .forms import GroupForm

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

def makeNewGroup(request):
    if request.method == "POST":
        form = GroupForm(request.POST)

        if form.is_valid():
            newGroup = Group()
            newGroup.name = form.cleaned_data["name"]
            newGroup.save()
            return HttpResponse("You've created a new group")

    else:
        form = GroupForm()

    return render(request, "makeNewGroup.html", {"form": form})
    
