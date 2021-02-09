from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class TodoList(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class TodoItem(models.Model):
    todoList = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    deadline = models.DateField()

    def __str__(self):
        return self.name