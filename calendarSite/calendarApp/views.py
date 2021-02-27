from django.shortcuts import render
from django.http import HttpResponse
from .models import Group, TodoList, TodoItem
from .forms import GroupForm, TodoListForm, TodoItemForm


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

def makeNewTodoList(request):
    groupList = Group.objects.all()
    print(len(groupList))

    if request.method == "POST":
        form = TodoListForm(request.POST)

        if form.is_valid():
            newTodoList = TodoList()
            parentGroup = Group.objects.get(name=form.cleaned_data["parent"]) 
            newTodoList.group = parentGroup
            newTodoList.name = form.cleaned_data["name"]
            newTodoList.save()
            return HttpResponse("You've created a new TodoList")


    else:
        form = TodoListForm()

    return render(request, "makeNewTodoList.html", {"form": form})

def makeNewTodoItem(request):
    if request.method == "POST":
        form = TodoItemForm(request.POST)

        if form.is_valid():
            newTodoItem = TodoItem()
            parentList = TodoList.objects.get(name=form.cleaned_data["parent"]) 
            newTodoItem.todoList = parentList
            newTodoItem.name = form.cleaned_data["name"]
            newTodoItem.deadline = form.cleaned_data["deadline"]
            newTodoItem.completed = False
            newTodoItem.save()
            return HttpResponse("You've created a new TodoItem")


    else:
        form = TodoItemForm()

    return render(request, "makeNewTodoItem.html", {"form": form})
    
