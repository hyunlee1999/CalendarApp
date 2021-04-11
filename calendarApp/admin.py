from django.contrib import admin

from .models import Group, TodoList, TodoItem

admin.site.register(Group)
admin.site.register(TodoList)
admin.site.register(TodoItem)