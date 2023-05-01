from django.urls import path
from app_custom_user.views import UserCreateView # UserListView,

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='user_create'),
    ]
