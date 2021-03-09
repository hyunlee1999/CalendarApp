from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    #Make Groups
    path("makeNewGroup", views.makeNewGroup, name="makeNewGroup"),
    path("makeNewTodoList", views.makeNewTodoList, name="makeNewTodoList"),
    path("makeNewTodoItem", views.makeNewTodoItem, name="makeNewTodoItem"),

    #Group Details
    path("<str:group>/", views.groupDetail, name="groupDetail"),
    path("<str:group>/<str:todoList>/", views.todoListDetail, name="todoListDetail"),
    path("<str:group>/<str:todoList>/<str:todoItem>/", views.todoItemDetail, name="todoItemDetail"),
    
    #Edit
    path("edit/<str:group_>", views.editGroup, name="editGroup"),
    path("edit/<str:group_>/<str:todoList_>", views.editTodoList, name="editTodoList"),

    #Ajax Requests
    path("ajax/delete", views.delete, name="delete"),

]