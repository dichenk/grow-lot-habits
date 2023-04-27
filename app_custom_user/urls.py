from django.urls import path
from app_custom_user.views import UserCreateView # UserListView,

urlpatterns = [
    # path('', UserListView.as_view(), name='user_list'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    ]
