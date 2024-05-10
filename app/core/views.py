"""
Views for the todo APIs
"""
from django.http.response import HttpResponse
from django.shortcuts import redirect
from core.models import Todo
from django.http import Http404

from django.shortcuts import render


def home(request):
    if not request.user.is_authenticated:
        return redirect('api/login')
    try:
        # todos = Todo.objects.all().order_by('created_at')
        todos = Todo.objects.all().filter(user=request.user).order_by('created_at')
        todo_count = todos.count()
    except Todo.DoesNotExist:
        raise Http404("not exist")
    context = {

        'todos': todos,
        'todo_count': todo_count
    }
    return render(request, 'index.html', context)
