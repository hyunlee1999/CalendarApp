from django import forms
from .models import Group, TodoList, TodoItem
from django.core.exceptions import ValidationError
from .validators import validate_name



class GroupForm(forms.Form):
    name = forms.CharField(label="Group Name", max_length=100, validators=[validate_name])
    previous = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleanedData = super(GroupForm, self).clean()
        nameCleaned = cleanedData.get("name")
        if Group.objects.filter(name=nameCleaned).exists():
            raise ValidationError ("Error: A  group with that name already exists")

        if "previous" in self.initial:
            cleanedData["previous"] = self.initial["previous"]

        return cleanedData

class TodoListForm(forms.Form):        
    parent= forms.ModelChoiceField(label = "Parent Group", queryset = Group.objects.all())
    name = forms.CharField(label="Todo List Name", max_length=100, validators=[validate_name])
    previousParent = forms.CharField(widget=forms.HiddenInput(), required=False)
    previousName = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleanedData = super().clean()
        nameCleaned = cleanedData.get("name")
        parentCleaned = cleanedData.get("parent")
        if TodoList.objects.filter(name=nameCleaned, group=parentCleaned).exists():
            error = "Error: A Todo List with that name already exists in group " + str(parentCleaned)
            raise ValidationError (error)

        if "previousParent" in self.initial:
            cleanedData["previousParent"] = self.initial["previousParent"]

        if "previousName" in self.initial:
            cleanedData["previousName" ] = self.initial["previousName"]

        return cleanedData


        
class TodoItemForm(forms.Form):
    parent= forms.ModelChoiceField(label = "Parent Todo List", queryset = TodoList.objects.all()) <br>
    name = forms.CharField(label="Todo Item Name:", max_length=100, validators=[validate_name])
    deadline = forms.DateField(widget = forms.SelectDateWidget(), label="(Optional) Deadline:", required=False)
    description = forms.CharField(label="(Optional) Description:", max_length=200, required=False)
    previousParent = forms.CharField(widget=forms.HiddenInput(), required=False)
    previousName = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleanedData = super().clean()
        nameCleaned = cleanedData.get("name")
        parentList = cleanedData.get("parent")
        if TodoItem.objects.filter(name=nameCleaned, todoList=parentList).exists() and cleanedData.get("previousName") != cleanedData.get("name"):
            raise ValidationError ("Error: A Todo Item with that name already exists in " + str(parentList) + " list")

        if "previousParent" in self.initial:
            cleanedData["previousParent"] = self.initial["previousParent"]

        if "previousName" in self.initial:
            cleanedData["previousName" ] = self.initial["previousName"]