from django import forms

class GroupForm(forms.Form):
    name = forms.CharField(label="Group Name", max_length=100)