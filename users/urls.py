from django.urls import path
from users.views import UserCreateView, LoginView


app_name = 'users'

urlpatterns = [
    path('', UserCreateView.as_view(), name='user_create'),
    path('login/', LoginView.as_view(), name='login'),
]