"""
Views for the todo APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication  # noqa
from rest_framework.permissions import IsAuthenticated  # noqa
from django.http.response import HttpResponse

from core.models import Todo
from todo import serializers
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer


class TodoViewSet(viewsets.ModelViewSet):
    """View for manage todo APIs."""
    serializer_class = serializers.TodoDetailSerializer
    queryset = Todo.objects.all()
    """Decomment if you want to try TokenAuthentication
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    """
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'partials/todo.html'

    def get_queryset(self):
        """Retrieve todos for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('created_at')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.TodoSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        todo = self.get_serializer(data=request.data)
        todo_count = self.get_queryset().count()
        todo.is_valid(raise_exception=True)
        self.perform_create(todo)
        if request.accepted_renderer.format == 'html':
            return Response({"todo": todo.data, "todo_count": todo_count})
        return Response(todo.data)

    def perform_create(self, serializer):
        """Create a new todo."""
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = not instance.status
        instance.save()
        todo = self.get_serializer(instance)
        if request.accepted_renderer.format == 'html':
            return Response({"todo": todo.data})
        return Response(todo.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return HttpResponse()

    def perform_destroy(self, instance):
        instance.delete()
