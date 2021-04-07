from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Group, TodoList, TodoItem
from .forms import GroupForm, TodoListForm, TodoItemForm, SignUpForm
from django.http import JsonResponse
from django.shortcuts import redirect, render
import datetime



@login_required
def index(request):
    groups = Group.objects.filter(user=request.user)
    todoLists = TodoList.objects.filter(user=request.user)
    todoItems = TodoItem.objects.filter(user=request.user)

    context = {
        "groups": groups,
        "todoLists": todoLists,
        "todoItems": todoItems,
    }

    return render(request, "index.html", context=context)

@login_required
def makeNewGroup(request):
    if request.method == "POST":
        form = GroupForm(request.POST)

        if form.is_valid():
            newGroup = Group()
            newGroup.name = form.cleaned_data["name"]
            newGroup.user = request.user
            newGroup.save()

            return redirect("/%s/" % newGroup.name)

    else:
        form = GroupForm()

    return render(request, "makeNewGroup.html", {"form": form})

@login_required
def makeNewTodoList(request, group=None):

    #groupList = Group.objects.all()

    if group != None:
        
        initial_dict = {
            "parent": Group.objects.get(name=group, user=request.user),
        }

    else:
        initial_dict = {}

    if request.method == "POST":
        form = TodoListForm(request.POST, initial=initial_dict)

        if form.is_valid():
            newTodoList = TodoList()
            parentGroup = Group.objects.get(name=form.cleaned_data["parent"], user=request.user) 
            newTodoList.group = parentGroup
            newTodoList.name = form.cleaned_data["name"]
            newTodoList.user = request.user
            newTodoList.save()
            return redirect("/%s/%s" % (parentGroup, newTodoList.name))

    else:
        form = TodoListForm(initial=initial_dict)

    return render(request, "makeNewTodoList.html", {"form": form})

@login_required
def makeNewTodoItem(request, group=None, todoList=None):

    if group != None:

        group =  Group.objects.get(name=group, user=request.user)
        todoList = TodoList.objects.get(name=todoList, group=group, user=request.user)
        
        initial_dict = {
            "parent": todoList,
            "importanceLevel": 0,
        }

    else:
        initial_dict = {
            "importanceLevel": 0,
        }

    if request.method == "POST":
        form = TodoItemForm(request.POST)

        if form.is_valid():
            newTodoItem = TodoItem()
            parentList = TodoList.objects.get(name=form.cleaned_data["parent"], user=request.user) 
            newTodoItem.todoList = parentList
            newTodoItem.name = form.cleaned_data["name"]
            newTodoItem.deadline = form.cleaned_data["deadline"]
            newTodoItem.description = form.cleaned_data["description"]
            newTodoItem.importanceLevel = form.cleaned_data["importanceLevel"]
            newTodoItem.completed = False
            newTodoItem.user = request.user
            newTodoItem.save()
            return redirect("/%s/%s/%s" % (parentList.group, parentList.name, newTodoItem.name))


    else:
        form = TodoItemForm(initial=initial_dict)

    return render(request, "makeNewTodoItem.html", {"form": form})

@login_required
def groupDetail(request, group):
    group = get_object_or_404(Group, name=group, user=request.user)
    childLists = TodoList.objects.all().filter(group=group, user=request.user)
    todoItems = TodoItem.objects.all().filter(completed=False, user=request.user)
    return render(request, "groupDetail.html", {"group": group, "todoLists": childLists, "todoItems": todoItems})

@login_required   
def todoListDetail(request, group, todoList):
    group = get_object_or_404(Group, name=group, user=request.user)
    todoList = get_object_or_404(TodoList, name=todoList, group=group, user=request.user)
    childItems = TodoItem.objects.all().filter(todoList = todoList, completed=False, user=request.user)
        
    return render(request, "todoListDetail.html", {"group": group, "todoList": todoList, "todoItems": childItems})

@login_required
def todoItemDetail(request, group, todoList, todoItem):
    group = get_object_or_404(Group, name=group, user=request.user)
    todoList = get_object_or_404(TodoList, name=todoList, group=group, user=request.user)
    todoItem = get_object_or_404(TodoItem, name=todoItem, todoList=todoList, user=request.user)
    return render(request, "todoItemDetail.html", {"group": group, "todoList": todoList, "todoItem": todoItem})

@login_required
def uncompletedItems(request):
    todoItems = TodoItem.objects.all().filter(completed=False, user=request.user)
    
    return render(request, "uncompletedItems.html", {"todoItems": todoItems})

@login_required
def completedItems(request):
    todoItems = TodoItem.objects.all().filter(completed=True, user=request.user)

    today = datetime.date.today()
    week = today - datetime.timedelta(days=7)
    thirty = today - datetime.timedelta(days=30)
    year = today - datetime.timedelta(days=365)

    todayCount = weekCount = thirtyCount = yearCount = 0

    for todoItem in todoItems:
        completedDate = todoItem.completedDate
        if  completedDate == today:
            todayCount = todayCount + 1
        if week <= completedDate <= today:
            weekCount = weekCount + 1
        if thirty <= completedDate <= today:
            thirtyCount = thirtyCount + 1
        if year <= completedDate <= today:
            yearCount = yearCount + 1
    
    return render(request, "completedItems.html", 
        {
            "todoItems": todoItems,
            "todayCount": todayCount,
            "weekCount": weekCount,
            "thirtyCount": thirtyCount,
            "yearCount": yearCount,
        })

@login_required
def delete(request):
    type = request.GET.get("type")
    name = request.GET.get("name")
    if (type == "group"):

        object = Group.objects.all().get(name = name, user=request.user)
        object.delete()

        data = {
            "isDeleted":True,
        }

        return JsonResponse(data)

    elif (type == "todoList"):
        groupName = request.GET.get("groupName")
        print(type, name, groupName)

        group = Group.objects.all().get(name= groupName, user=request.user)


        object = TodoList.objects.all().get(group= group, name = name, user=request.user)
        object.delete()

        data = {
            "isDeleted":True,
        }

        return JsonResponse(data)

    elif (type == "todoItem"):
        object = TodoItem.objects.all().get(name = name, user=request.user)
        object.delete()
    
    data = {
        "isDeleted":True,
    }

    return JsonResponse(data)

@login_required
def completed(request):
    name = request.GET.get("name")
   
    object = TodoItem.objects.all().get(name = name, user=request.user)
    object.completedDate = datetime.date.today()
    object.completed = True
    object.save()

    data = {}
    
    return JsonResponse(data)

@login_required
def uncompleted(request):
    name = request.GET.get("name")
   
    object = TodoItem.objects.all().get(name = name, user=request.user)
    object.completed = False
    object.completedDate = None
    object.save()

    data = {}
    
    return JsonResponse(data)

@login_required
def editGroup(request, group_):

    if request.method == "POST":

        initial_dict = {
            "previous": group_,
        }

        form = GroupForm(request.POST, initial=initial_dict)

        if form.is_valid():
            groupName = form.cleaned_data["previous"]
            group = get_object_or_404(Group, name=groupName, user=request.user)
            group.name =  form.cleaned_data["name"]
            group.save()

            return redirect("/%s/" % group.name)

    else:
        initial_dict = {
            "name": group_,
            "previous": group_,
        }

        group = get_object_or_404(Group, name=group_, user=request.user)
        form = GroupForm(initial=initial_dict)

    return render(request, "editGroup.html", {"form": form, "group": group.name})

@login_required
def editTodoList(request, group_, todoList_):

    initial_dict = {
        "name": todoList_,
        "parent": get_object_or_404(Group, name=group_, user=request.user),
        "previousParent": group_,
        "previousName": todoList_,
    }

    if request.method == "POST":

        form = TodoListForm(request.POST, initial=initial_dict)

        if form.is_valid():
            previousName = form.cleaned_data["previousName"]
            previousParent = form.cleaned_data["previousParent"]
            previousParent = get_object_or_404(Group, name=previousParent, user=request.user)
            todoList = get_object_or_404(TodoList, name=previousName, group=previousParent, user=request.user)
            todoList.name =  form.cleaned_data["name"]
            todoList.group = get_object_or_404(Group, name=form.cleaned_data["parent"], user=request.user)
            todoList.save()

            return redirect("/%s/%s" % (todoList.group, todoList.name))
            
    else:
        group =  get_object_or_404(Group, name=group_, user=request.user)
        todoList = get_object_or_404(TodoList, name=todoList_, group=group, user=request.user)
        form = TodoListForm(initial=initial_dict)

    return render(request, "editTodoList.html", {"form": form, "group": todoList.group, "name": todoList.name})


@login_required
def editTodoItem(request, group_, todoList_, todoItem_):

    group = get_object_or_404(Group, name=group_, user=request.user)
    todoList = get_object_or_404(TodoList, name=todoList_, group= group, user=request.user)
    todoItem = get_object_or_404(TodoItem, name=todoItem_, todoList = todoList, user=request.user)

    initial_dict = {
        "name": todoItem.name,
        "parent": todoList,
        "previousParent": todoList.name,
        "previousName": todoItem.name,
        "deadline": todoItem.deadline,
        "description": todoItem.description,
        "importanceLevel": todoItem.importanceLevel,
    }

    if request.method == "POST":

        form = TodoItemForm(request.POST, initial=initial_dict)

        if form.is_valid():
            previousName = form.cleaned_data["previousName"]
            previousParent = form.cleaned_data["previousParent"]
            previousParent = get_object_or_404(TodoList, name=previousParent, user=request.user)
            todoItem = get_object_or_404(TodoItem, name=previousName, todoList=previousParent, user=request.user)
            todoItem.name =  form.cleaned_data["name"]
            todoItem.todoList = get_object_or_404(TodoList, name=form.cleaned_data["parent"])
            todoItem.description = form.cleaned_data["description"]
            todoItem.deadline = form.cleaned_data["deadline"]
            todoItem.importanceLevel = form.cleaned_data["importanceLevel"]

            todoItem.save()

            return redirect("/%s/%s/%s" % (todoList.group, todoList.name, todoItem.name))
            
    else:

        form = TodoItemForm(initial=initial_dict)

    return render(request, "editTodoItem.html", {"form": form, "group": todoList.group, "todoList": todoList.name, "name": todoItem.name})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")



