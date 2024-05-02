"""
Serializers for todo APIs
"""
from rest_framework import serializers

from core.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    """Serializer for todos."""

    class Meta:
        model = Todo
        fields = ['id', 'content', 'status',
                  'due_date', 'priority', 'created_at']
        read_only_fields = ['id']


class TodoDetailSerializer(TodoSerializer):
    """Serializer for todo detail view."""

    class Meta(TodoSerializer.Meta):
        fields = TodoSerializer.Meta.fields + ['content']
