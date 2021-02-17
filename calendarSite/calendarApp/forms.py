from django import forms
from .models import Group, TodoList, TodoItem

class GroupForm(forms.Form):
    name = forms.CharField(label="Group Name", max_length=100)

class TodoListForm(forms.Form):
    groupList = Group.objects.all()
    groupNames = []

    for group in groupList:
        name = group.name
        groupNames.append((name, name))

    groupNames = tuple(groupNames)
    
    parent= forms.CharField(label="Parent Group", widget=forms.Select(choices=groupNames))
    name = forms.CharField(label="Todo List Name", max_length=100)

class TodoItemForm(forms.Form):
    todoLists = TodoList.objects.all()
    todoListNames = []

    for todoList in todoLists:
        name = todoList.name
        todoListNames.append((name, name))

    todoListNames = tuple(todoListNames)
    
    parent = forms.CharField(label="Parent Todo List", widget=forms.Select(choices=todoListNames))
    name = forms.CharField(label="Todo Item Name", max_length=100)
    deadline = forms.DateField(widget = forms.SelectDateWidget(), label="Deadline:")