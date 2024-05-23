"""
URL mappings for the todo app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from todo import views


router = DefaultRouter()
router.register('', views.TodoViewSet)

app_name = 'todo'

urlpatterns = [
    path('todos/', include(router.urls)),
    path('', views.list_todos, name="todos"),
    path('create_todo/', views.create_todo, name="create_todo"),
    path('delete_todo/<int:pk>/', views.delete_todo, name="delete_todo"),
    path('update_todo/<int:pk>/', views.update_todo, name="update_todo"),
]
