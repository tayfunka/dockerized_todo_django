"""
Tests for todo APIs.
"""
import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Todo

from todo.serializers import (
    TodoSerializer,
    TodoDetailSerializer)

TODOS_URL = reverse('todo:todo-list')


def detail_url(todo_id):
    """Create and return a todo detail URL."""
    return reverse('todo:todo-detail', args=[todo_id])


def create_todo(user, **params):
    """Create and return a sample todo."""
    defaults = {
        'content': 'sample todo',
        'status': True,
        'priority': False,
        'due_date': timezone.now() + datetime.timedelta(days=1),
        'created_at': timezone.now() - datetime.timedelta(days=1)
    }
    defaults.update(params)

    todo = Todo.objects.create(user=user, **defaults)
    return todo


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicTodoAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(TODOS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTodoApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_todos(self):
        """Test retrieving a list of todos."""
        create_todo(user=self.user)
        create_todo(user=self.user)

        res = self.client.get(TODOS_URL)

        todos = Todo.objects.all().order_by('-id')
        serializer = TodoSerializer(todos, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_todo_list_limited_to_user(self):
        """Test list of todos is limited to authenticated user."""
        other_user = create_user(email='other@example.com', password='test123')
        create_todo(user=other_user)
        create_todo(user=self.user)

        res = self.client.get(TODOS_URL)

        todos = Todo.objects.filter(user=self.user)
        serializer = TodoSerializer(todos, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_todo_detail(self):
        """Test get todo detail.."""
        todo = create_todo(user=self.user)

        url = detail_url(todo.id)
        res = self.client.get(url)

        serializer = TodoDetailSerializer(todo)
        self.assertEqual(res.data, serializer.data)

    def test_mark_todo_as_completed(self):
        """Test status update of a todo."""
        todo = create_todo(
            user=self.user,
            content='test todo.',
            due_date=timezone.now() + datetime.timedelta(days=1),
            status=True,
            priority=False,
        )

        payload = {'status': False}
        url = detail_url(todo.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        todo.refresh_from_db()
        self.assertEqual(todo.status, payload['status'])

    def test_full_update(self):
        """Test full update of todo."""
        todo = create_todo(
            user=self.user,
            content='test todo.',
            due_date=timezone.now() + datetime.timedelta(days=1),
            status=True,
            priority=False,
        )

        payload = {
            'content': 'New test todo.',
            'due_date': timezone.now() + datetime.timedelta(days=1),
            'status': False,
            'priority': True,
        }
        url = detail_url(todo.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        todo.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(todo, k), v)
        self.assertEqual(todo.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the todo user results in an error."""
        new_user = create_user(email='test2@example.com', password='test123')
        todo = create_todo(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(todo.id)
        self.client.patch(url, payload)

        todo.refresh_from_db()
        self.assertEqual(todo.user, self.user)

    def test_delete_todo(self):
        """Test deleting a todo successful."""
        todo = create_todo(user=self.user)

        url = detail_url(todo.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Todo.objects.filter(id=todo.id).exists())

    def test_todo_other_users_todo_error(self):
        """Test trying to delete another users todo gives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        todo = create_todo(user=new_user)

        url = detail_url(todo.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Todo.objects.filter(id=todo.id).exists())

    def test_create_todo(self):
        """Test creating a todo."""
        payload = {
            'content': 'Sample todo',
            'status': True,
            'due_date': timezone.now() + datetime.timedelta(days=1),
            'priority': False,
        }
        res = self.client.post(TODOS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        todo = Todo.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(todo, k), v)
        self.assertEqual(todo.user, self.user)
