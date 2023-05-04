from django.db import models

# from app_custom_user.models import CustomUser
from author.decorators import with_author


@with_author
class Habit(models.Model):
    description = models.CharField(max_length=128, default='', verbose_name='description')
    created = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='habit created')
    place = models.CharField(max_length=128, default='', verbose_name='place')
    time = models.TimeField(max_length=100, default='12:00', verbose_name='time')
    action = models.CharField(max_length=128, default='', verbose_name='action')
    pleasure_habit = models.BooleanField(default=False, verbose_name='pleasure habit')
    binded_habit = models.CharField(max_length=128, default=None, verbose_name='binded habit', null=True, blank=True)
    periodic_habit = models.PositiveSmallIntegerField(default=7, verbose_name='periodic habit')
    reward = models.CharField(max_length=128, default=None, verbose_name='reward', null=True, blank=True)
    time_for_finishing = models.PositiveSmallIntegerField(default=1, verbose_name='time for finishing')
    is_public = models.BooleanField(default=False, verbose_name='public or not')
    date_notification = models.DateField(auto_now=False, auto_now_add=False, verbose_name='date_notification', null=True, blank=True)


    def __str__(self):
        return f'Habit {self.title}'

    class Meta:
        verbose_name = 'habit'
        verbose_name_plural = 'habitы'
