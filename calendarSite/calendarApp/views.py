from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Group, TodoList, TodoItem
from .forms import GroupForm, TodoListForm, TodoItemForm
from django.http import JsonResponse
from django.shortcuts import redirect
import datetime


def index(request):
    groups = Group.objects.all()
    todoLists = TodoList.objects.all()
    todoItems = TodoItem.objects.all()

    context = {
        "groups": groups,
        "todoLists": todoLists,
        "todoItems": todoItems,
    }

    return render(request, "index.html", context=context)

def makeNewGroup(request):
    if request.method == "POST":
        form = GroupForm(request.POST)

        if form.is_valid():
            newGroup = Group()
            newGroup.name = form.cleaned_data["name"]
            newGroup.save()

            return redirect("/%s/" % newGroup.name)

    else:
        form = GroupForm()

    return render(request, "makeNewGroup.html", {"form": form})

def makeNewTodoList(request, group=None):

    groupList = Group.objects.all()

    if group != None:
        
        initial_dict = {
            "parent": Group.objects.get(name=group),
        }

    else:
        initial_dict = {}

    if request.method == "POST":
        form = TodoListForm(request.POST, initial=initial_dict)

        if form.is_valid():
            newTodoList = TodoList()
            parentGroup = Group.objects.get(name=form.cleaned_data["parent"]) 
            newTodoList.group = parentGroup
            newTodoList.name = form.cleaned_data["name"]
            newTodoList.save()
            return redirect("/%s/%s" % (parentGroup, newTodoList.name))

    else:
        form = TodoListForm(initial=initial_dict)

    return render(request, "makeNewTodoList.html", {"form": form})

def makeNewTodoItem(request, group=None, todoList=None):

    if group != None:

        group =  Group.objects.get(name=group)
        todoList = TodoList.objects.get(name=todoList, group=group)
        
        initial_dict = {
            "deadline": datetime.date.today,
            "parent": todoList,
        }

    else:
        initial_dict = {
            "deadline": datetime.date.today,
        }

    if request.method == "POST":
        form = TodoItemForm(request.POST)

        if form.is_valid():
            newTodoItem = TodoItem()
            parentList = TodoList.objects.get(name=form.cleaned_data["parent"]) 
            newTodoItem.todoList = parentList
            newTodoItem.name = form.cleaned_data["name"]
            newTodoItem.deadline = form.cleaned_data["deadline"]
            newTodoItem.description = form.cleaned_data["description"]
            newTodoItem.completed = False
            newTodoItem.save()
            return redirect("/%s/%s/%s" % (parentList.group, parentList.name, newTodoItem.name))


    else:
        form = TodoItemForm(initial=initial_dict)

    return render(request, "makeNewTodoItem.html", {"form": form})

def groupDetail(request, group):
    group = get_object_or_404(Group, name=group)
    childLists = TodoList.objects.all().filter(group=group)
    todoItems = TodoItem.objects.all().filter(completed=False)
    return render(request, "groupDetail.html", {"group": group, "todoLists": childLists, "todoItems": todoItems})
    
def todoListDetail(request, group, todoList):
    group = get_object_or_404(Group, name=group)
    todoList = get_object_or_404(TodoList, name=todoList, group=group)
    childItems = TodoItem.objects.all().filter(todoList = todoList, completed=False)
        
    return render(request, "todoListDetail.html", {"group": group, "todoList": todoList, "todoItems": childItems})

def todoItemDetail(request, group, todoList, todoItem):
    group = get_object_or_404(Group, name=group)
    todoList = get_object_or_404(TodoList, name=todoList, group=group)
    todoItem = get_object_or_404(TodoItem, name=todoItem, todoList=todoList)
    return render(request, "todoItemDetail.html", {"group": group, "todoList": todoList, "todoItem": todoItem})

def completedItems(request):
    todoItems = TodoItem.objects.all().filter(completed=True)
    return render(request, "completedItems.html", {"todoItems": todoItems})

def delete(request):
    type = request.GET.get("type")
    name = request.GET.get("name")
    if (type == "group"):

        object = Group.objects.all().get(name = name)
        object.delete()

        data = {
            "isDeleted":True,
        }

        return JsonResponse(data)

    elif (type == "todoList"):
        object = TodoList.objects.all().get(name = name)
        object.delete()

        data = {
            "isDeleted":True,
        }

        return JsonResponse(data)

    elif (type == "todoItem"):
        object = TodoItem.objects.all().get(name = name)
        object.delete()
    
    data = {
        "isDeleted":True,
    }

    return JsonResponse(data)

def completed(request):
    name = request.GET.get("name")
   
    object = TodoItem.objects.all().get(name = name)
    object.completed = True
    object.save()

    data = {}
    
    return JsonResponse(data)

def uncompleted(request):
    name = request.GET.get("name")
   
    object = TodoItem.objects.all().get(name = name)
    object.completed = False
    object.save()

    data = {}
    
    return JsonResponse(data)

def editGroup(request, group_):

    if request.method == "POST":

        initial_dict = {
            "previous": group_,
        }

        form = GroupForm(request.POST, initial=initial_dict)

        if form.is_valid():
            groupName = form.cleaned_data["previous"]
            group = get_object_or_404(Group, name=groupName)
            group.name =  form.cleaned_data["name"]
            group.save()

            return redirect("/%s/" % group.name)

    else:
        initial_dict = {
            "name": group_,
            "previous": group_,
        }

        group = get_object_or_404(Group, name=group_)
        form = GroupForm(initial=initial_dict)

    return render(request, "editGroup.html", {"form": form, "group": group.name})


def editTodoList(request, group_, todoList_):

    initial_dict = {
        "name": todoList_,
        "parent": get_object_or_404(Group, name=group_),
        "previousParent": group_,
        "previousName": todoList_,
    }

    if request.method == "POST":

        form = TodoListForm(request.POST, initial=initial_dict)

        if form.is_valid():
            previousName = form.cleaned_data["previousName"]
            previousParent = form.cleaned_data["previousParent"]
            previousParent = get_object_or_404(Group, name=previousParent)
            todoList = get_object_or_404(TodoList, name=previousName, group=previousParent)
            todoList.name =  form.cleaned_data["name"]
            todoList.group = get_object_or_404(Group, name=form.cleaned_data["parent"])
            todoList.save()

            return redirect("/%s/%s" % (todoList.group, todoList.name))
            
    else:
        group =  get_object_or_404(Group, name=group_)
        todoList = get_object_or_404(TodoList, name=todoList_, group=group)
        form = TodoListForm(initial=initial_dict)

    return render(request, "editTodoList.html", {"form": form, "group": todoList.group, "name": todoList.name})


def editTodoItem(request, group_, todoList_, todoItem_):

    group = get_object_or_404(Group, name=group_)
    todoList = get_object_or_404(TodoList, name=todoList_, group= group)
    todoItem = get_object_or_404(TodoItem, name=todoItem_, todoList = todoList)

    initial_dict = {
        "name": todoItem.name,
        "parent": todoList,
        "previousParent": todoList.name,
        "previousName": todoItem.name,
        "deadline": todoItem.deadline,
        "description": todoItem.description,
    }

    if request.method == "POST":

        form = TodoItemForm(request.POST, initial=initial_dict)

        if form.is_valid():
            previousName = form.cleaned_data["previousName"]
            previousParent = form.cleaned_data["previousParent"]
            previousParent = get_object_or_404(TodoList, name=previousParent)
            todoItem = get_object_or_404(TodoItem, name=previousName, todoList=previousParent)
            todoItem.name =  form.cleaned_data["name"]
            todoItem.todoList = get_object_or_404(TodoList, name=form.cleaned_data["parent"])
            todoItem.description = form.cleaned_data["description"]
            todoItem.deadline = form.cleaned_data["deadline"]

            todoItem.save()

            return redirect("/%s/%s/%s" % (todoList.group, todoList.name, todoItem.name))
            
    else:

        form = TodoItemForm(initial=initial_dict)

    return render(request, "editTodoItem.html", {"form": form, "group": todoList.group, "todoList": todoList.name, "name": todoItem.name})