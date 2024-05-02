"""
Views for the todo APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Todo
from todo import serializers


class TodoViewSet(viewsets.ModelViewSet):
    """View for manage todo APIs."""
    serializer_class = serializers.TodoDetailSerializer
    queryset = Todo.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve todos for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.TodoSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new todo."""
        serializer.save(user=self.request.user)
