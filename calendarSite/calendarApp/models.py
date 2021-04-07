from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class TodoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def getGroup(self):
        return str(self.group)


class TodoItem(models.Model):
    CHOICES = [(i,i) for i in range(4)]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todoList = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True)
    completed = models.BooleanField(default=False)
    completedDate = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    importanceLevel = models.IntegerField(default=0, choices=CHOICES)

    def __str__(self):
        return self.name

    def getTodoList(self):
        return str(self.todoList)
    