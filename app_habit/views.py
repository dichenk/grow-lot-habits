from rest_framework import generics
from app_habit.models import Habit
from app_habit.serializers import HabitCreateSerializer, HabitViewSerializer, HabitDeleteSerializer, \
    HabitUpdateSerializer
from app_habit.permissions import Owner


class HabitCreateView(generics.CreateAPIView):
    serializer_class = HabitCreateSerializer


class HabitListView(generics.ListAPIView):  # for testing
    serializer_class = HabitViewSerializer

    def get_queryset(self):
        queryset = Habit.objects.all()
        queryset = queryset.filter(is_public=True)
        return queryset


class MyHabitListView(generics.ListAPIView):  # for testing
    serializer_class = HabitViewSerializer

    def get_queryset(self):
        queryset = Habit.objects.all()
        queryset = queryset.filter(author=self.request.user)
        return queryset


class HabitDeleteView(generics.DestroyAPIView):
    serializer_class = HabitDeleteSerializer
    queryset = Habit.objects.all()
    permission_classes = [Owner]


class HabitUpdateView(generics.UpdateAPIView):
    model = Habit
    queryset = Habit.objects.all()
    serializer_class = HabitUpdateSerializer
    permission_classes = [Owner]