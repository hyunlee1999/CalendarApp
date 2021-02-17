from django import forms
from .models import Group, TodoList, TodoItem

class GroupForm(forms.Form):
    name = forms.CharField(label="Group Name", max_length=100)

class TodoListForm(forms.Form):
    groupList = Group.objects.all()
    groupNames = []

    for group in groupList:
        name = group.name
        groupNames.append(name)
    
    groupNames = tuple(groupNames)

    parentGroup = forms.ChoiceField(choices=groupNames)
    name = forms.CharField(label="Todo List Name", max_length=100)
