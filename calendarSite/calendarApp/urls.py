from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("makeNewGroup", views.makeNewGroup, name="makeNewGroup"),
    path("makeNewTodoList", views.makeNewTodoList, name="makeNewTodoList"),
]