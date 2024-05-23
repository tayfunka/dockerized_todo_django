"""
Views for the todo APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication  # noqa
from rest_framework.permissions import IsAuthenticated  # noqa

from core.models import Todo
from todo import serializers

from django.views.generic import ListView
from django.views.decorators.http import require_http_methods
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


class TodoViewSet(viewsets.ModelViewSet):
    """View for manage todo APIs."""
    serializer_class = serializers.TodoDetailSerializer
    queryset = Todo.objects.all()
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve todos for authenticated user."""
        return self.queryset.filter(
            user=self.request.user).order_by('created_at')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.TodoSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new todo."""
        serializer.save(user=self.request.user)

    # def partial_update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.status = not instance.status
    #     instance.save()
    #     todo = self.get_serializer(instance)
    #     return Response(todo.data)


@login_required(redirect_field_name='next', login_url="/user/login")
class TodoListView(ListView):
    """View for List Todos"""
    model = Todo
    context_object_name = "todos"
    template_name = "todo/todos.html"


@login_required(redirect_field_name='next', login_url="/user/login")
@require_http_methods(['GET'])
def list_todos(request):
    todos = Todo.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "todo/todos.html", {"todos": todos})


@login_required(redirect_field_name='next', login_url="/user/login")
@require_http_methods(['POST'])
def create_todo(request):
    if request.method == "POST":
        content = request.POST.get("content", "")

        if content:
            todo = Todo.objects.create(
                user=request.user, content=content, status=False)

        return render(request, "todo/partials/todo.html", {"todo": todo})


@login_required(redirect_field_name='next', login_url="/user/login")
@require_http_methods(['PUT'])
def update_todo(request, pk):
    todo = Todo.objects.get(pk=pk)
    todo.status = not todo.status
    todo.save()
    return render(request, "todo/partials/todo.html", {"todo": todo})


@login_required(redirect_field_name='next', login_url="/user/login")
@require_http_methods(['DELETE'])
def delete_todo(request, pk):
    todo = Todo.objects.get(pk=pk)
    todo.delete()

    return HttpResponse()
