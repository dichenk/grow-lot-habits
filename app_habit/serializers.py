from rest_framework import serializers
from app_habit.models import Habit
from app_habit.validators import HabitValidator


class HabitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = (
            'time',
            'place',
            'action',
            'reward',
            'time_for_finishing',
            'periodic_habit',
            'pleasure_habit',
            'binded_habit',
            'is_public'
        )
        validators = [HabitValidator(field='model')]


class HabitViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'


class HabitDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ('id')


class HabitUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'