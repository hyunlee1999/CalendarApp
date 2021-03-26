from calendarApp.models import Group, TodoList, TodoItem

def count(request):
    return {
        'num_Group': Group.objects.all().count(),
        'num_TodoList': TodoList.objects.all().count(),
        'num_TodoItem': TodoItem.objects.filter(completed=False).count(),
    }