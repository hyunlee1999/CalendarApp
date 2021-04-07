from calendarApp.models import Group, TodoList, TodoItem

def count(request):
    if request.user.is_authenticated:
        return {
            'num_Group': Group.objects.filter(user=request.user).count(),
            'num_TodoList': TodoList.objects.all().count(),
            'num_TodoItem': TodoItem.objects.filter(completed=False).count(),
        }
    else:
        return {
            'num_Group': 0,
            'num_TodoList':0,
            'num_TodoItem': 0,
        }