from calendarApp.models import Group, TodoList, TodoItem
from django.contrib.auth.models import User


def count(request):
    if request.user.is_authenticated:
        return {
            'num_Group': Group.objects.filter(user=request.user).count(),
            'num_TodoList': TodoList.objects.filter(user=request.user).count(),
            'num_TodoItem': TodoItem.objects.filter(user=request.user, completed=False).count(),
        }
    else:
        return {
            'num_Group': 0,
            'num_TodoList':0,
            'num_TodoItem': 0,
        }