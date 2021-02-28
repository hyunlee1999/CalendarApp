from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Group, TodoList, TodoItem
from .forms import GroupForm, TodoListForm, TodoItemForm


#need to throw an error if there the users make a name that is already in the database.
#Also need to code some of the things if it is empty


def index(request):

    '''

    TodoItem.objects.all().delete()
    TodoList.objects.all().delete()
    Group.objects.all().delete()

        '''



    num_Groups = Group.objects.all().count()
    num_TodoList = TodoList.objects.all().count()
    num_TodoItem = TodoItem.objects.all().count()
    groups = Group.objects.all()
    todoLists = TodoList.objects.all()
    todoItems = TodoItem.objects.all()

    context = {
        "num_Groups": num_Groups,
        "num_TodoList": num_TodoList,
        "num_TodoItem": num_TodoItem,
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
            return HttpResponse("You've created a new group")

    else:
        form = GroupForm()

    return render(request, "makeNewGroup.html", {"form": form})

def makeNewTodoList(request):
    groupList = Group.objects.all()

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
            parentList = TodoList.objects.get(name=form.cleaned_data["parentList"]) 
            newTodoItem.todoList = parentList
            newTodoItem.name = form.cleaned_data["name"]
            newTodoItem.deadline = form.cleaned_data["deadline"]
            newTodoItem.completed = False
            newTodoItem.save()
            return HttpResponse("You've created a new TodoItem")


    else:
        form = TodoItemForm()

    return render(request, "makeNewTodoItem.html", {"form": form})

def groupDetail(request, group):
    group = get_object_or_404(Group, name=group)
    childLists = TodoList.objects.all().filter(group=group)
    return render(request, "groupDetail.html", {"group": group, "todoLists": childLists})
    
def todoListDetail(request, group, todoList):
    group = get_object_or_404(Group, name=group)
    todoList = get_object_or_404(TodoList, name=todoList, group=group)
    childItems = TodoItem.objects.all().filter(todoList = todoList)
    return render(request, "todoListDetail.html", {"group": group, "todoList": todoList, "todoItems": childItems})

def todoItemDetail(request, group, todoList, todoItem):
    group = get_object_or_404(Group, name=group)
    todoList = get_object_or_404(TodoList, name=todoList, group=group)
    todoItem = get_object_or_404(TodoItem, name=todoItem, todoList=todoList)
    return render(request, "todoItemDetail.html", {"group": group, "todoList": todoList, "todoItem": todoItem})
    
