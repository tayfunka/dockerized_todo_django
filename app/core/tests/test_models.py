"""
Tests for models.
"""
import datetime
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is ok."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_todo(self):
        """Test creating a todo is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )
        todo = models.Todo.objects.create(
            user=user,
            content='Test todo',
            status=True,
            priority=False,
            due_date=timezone.now() + datetime.timedelta(days=1),
            created_at=timezone.now() - datetime.timedelta(days=1)
        )

        self.assertEqual(str(todo), todo.content)

    def test_mark_as_completed(self):
        """Test marking a todo as completed."""
        user = get_user_model().objects.create(
            email='test@example.com',
            password='testpass123',
        )
        todo = models.Todo.objects.create(
            user=user,
            content='Test todo',
            status=True,
            priority=False
        )
        todo.mark_as_completed()

        self.assertFalse(todo.status)

    def test_mark_as_high_priority(self):
        """Test marking a todo as high priority."""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        todo = models.Todo.objects.create(
            user=user,
            content='Test todo',
            status=True,
            priority=False
        )
        todo.mark_as_high_priority()

        self.assertTrue(todo.priority)


def test_was_created_recently(self):
    """Test checking if a todo was created recently."""
    user = get_user_model().objects.create_user(
        email='test@example.com',
        password='testpass123'
    )

    created_at_recent = timezone.now() - datetime.timedelta(days=1)
    todo_recent = models.Todo.objects.create(
        user=user,
        content='Test todo',
        status=True,
        priority=False,
        created_at=created_at_recent
    )

    self.assertTrue(todo_recent.was_created_recently())
    self.assertEqual(todo_recent.created_at, created_at_recent)

    created_at_past = timezone.now() - datetime.timedelta(days=2)
    todo_past = models.Todo.objects.create(
        user=user,
        content='Test todo 2',
        status=True,
        priority=False,
        created_at=created_at_past
    )

    self.assertFalse(todo_past.was_created_recently())
    self.assertEqual(todo_past.created_at, created_at_past)