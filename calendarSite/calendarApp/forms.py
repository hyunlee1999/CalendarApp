from django import forms
from .models import Group, TodoList, TodoItem
from django.core.exceptions import ValidationError
from .validators import validate_name



class GroupForm(forms.Form):
    name = forms.CharField(label="Group Name", max_length=100, validators=[validate_name])

    def clean(self):
        cleanedData = super().clean()
        nameCleaned = cleanedData.get("name")
        if Group.objects.filter(name=nameCleaned).exists():
            raise ValidationError ("Error: A  group with that name already exists")

class EditGroupForm(forms.Form):
    previous = forms.CharField(label="You are editing this field", disabled=True)
    name = forms.CharField(label="Group Name", max_length=100, validators=[validate_name])


    def clean(self):
        cleanedData = super().clean()
        nameCleaned = cleanedData.get("name")
        if Group.objects.filter(name=nameCleaned).exists():
            raise ValidationError ("Error: A  group with that name already exists")

class TodoListForm(forms.Form):        
    parent= forms.ModelChoiceField(label = "Parent Group", queryset = Group.objects.all())
    name = forms.CharField(label="Todo List Name", max_length=100, validators=[validate_name])

    def clean(self):
        cleanedData = super().clean()
        nameCleaned = cleanedData.get("name")
        parentCleaned = cleanedData.get("parent")
        if TodoList.objects.filter(name=nameCleaned, group=parentCleaned).exists():
            error = "Error: A Todo List with that name already exists in group " + str(parentCleaned)
            raise ValidationError (error)


        
class TodoItemForm(forms.Form):

    parentList= forms.ModelChoiceField(label = "Parent Todo List", queryset = TodoList.objects.all())
    name = forms.CharField(label="Todo Item Name", max_length=100, validators=[validate_name])
    deadline = forms.DateField(widget = forms.SelectDateWidget(), label="Deadline:")

    def clean(self):
        cleanedData = super().clean()
        nameCleaned = cleanedData.get("name")
        parentList = cleanedData.get("parentList")
        if TodoItem.objects.filter(name=nameCleaned, todoList=parentList).exists():
            raise ValidationError ("Error: A Todo Item with that name already exists in" + str(parentList) + "list")