from app_habit.views import HabitCreateView, HabitListView, HabitDeleteView, HabitUpdateView, MyHabitListView
from django.urls import path


urlpatterns = [
        path('', HabitListView.as_view(), name='habit_list'),
        path('mine/', MyHabitListView.as_view(), name='my_habit_list'),
        path('create/', HabitCreateView.as_view(), name='habit_create'),
        path('delete/<int:pk>/', HabitDeleteView.as_view(), name='habit_delete'),
        path('update/<int:pk>/', HabitUpdateView.as_view(), name='habit_update')
        ]

