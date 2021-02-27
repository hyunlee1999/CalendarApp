from django import forms
from .models import Group, TodoList, TodoItem

class GroupForm(forms.Form):
    name = forms.CharField(label="Group Name", max_length=100)

class TodoListForm(forms.Form):        
    parent= forms.ModelChoiceField(label = "Parent Group", queryset = Group.objects.all())
    name = forms.CharField(label="Todo List Name", max_length=100)

class TodoItemForm(forms.Form):
    parent= forms.ModelChoiceField(label = "Parent Todo List", queryset = TodoList.objects.all())
    name = forms.CharField(label="Todo Item Name", max_length=100)
    deadline = forms.DateField(widget = forms.SelectDateWidget(), label="Deadline:")