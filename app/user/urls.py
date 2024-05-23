"""
URL mappings for the user API.
"""
from django.urls import path

from user import views
from django.contrib.auth import views as auth_views
# from user.views import CreateUserView

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('login/', auth_views.LoginView.as_view(
        template_name='user/login.html'),
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('register/', CreateUserView.as_view(), name='register'),
]
