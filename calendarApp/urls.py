from django.urls import path
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    path('', views.index, name='index'),

    #Create
    path("makeNewGroup", views.makeNewGroup, name="makeNewGroup"),
    path("makeNewTodoList", views.makeNewTodoList, name="makeNewTodoList"),
    path("makeNewTodoItem", views.makeNewTodoItem, name="makeNewTodoItem"),

    #Add New
    path("add/<str:group>", views.makeNewTodoList, name="addNewGroup"),
    path("add/<str:group>/<str:todoList>", views.makeNewTodoItem, name="addNewGroup"),

    #Details
    path("<str:group>/", views.groupDetail, name="groupDetail"),
    path("<str:group>/<str:todoList>/", views.todoListDetail, name="todoListDetail"),
    path("<str:group>/<str:todoList>/<str:todoItem>/", views.todoItemDetail, name="todoItemDetail"),



    
    #Edit
    path("edit/<str:group_>", views.editGroup, name="editGroup"),
    path("edit/<str:group_>/<str:todoList_>", views.editTodoList, name="editTodoList"),
    path("edit/<str:group_>/<str:todoList_>/<str:todoItem_>", views.editTodoItem, name="editTodoItem"),


    #complete/uncomplete    
    path("completed", views.completedItems, name="completedItems"),
    path("uncompleted", views.uncompletedItems, name="uncompletedItems"),
    path("signup", views.signup, name="signup"),
    path("login", auth_views.LoginView.as_view(template_name="login.html"), {'next_page': '/'}, name="login"),
    path("logout", views.logout_view, name='logout'),
    path("demo", views.demo, name="demo"),
    #Ajax Requests
    path("ajax/delete", views.delete, name="delete"),
    path("ajax/completed", views.completed, name="completed"),
    path("ajax/uncompleted", views.uncompleted, name="uncompleted"),

]