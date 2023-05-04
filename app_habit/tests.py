from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from app_habit.urls import *
from app_custom_user.urls import *


class HabitTestCase(APITestCase):
    client = APIClient()

    def setUp(self):  # creating user, habit
        resp = self.client.post(reverse('user_create'), {
            'email': 'kokoko@bebe.be',
            'password': 'test123'})
        resp = self.client.post(reverse('token_obtain_pair'), {'email': 'kokoko@bebe.be', 'password': 'test123'},
                                format='json')
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_habit_create(self):
        resp = self.client.post(reverse('habit_create'), {
            "time": "17:00",
            "place": "place",
            "action": "action",
            "reward": "reward",
            "time_for_finishing": 2,
            "periodic_habit": 4,
            "pleasure_habit": False,
            "is_public": True
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_lesson_view(self):
        self.test_habit_create()
        resp = self.client.get(reverse('habit_list'), data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_mine_lesson_view(self):
        self.test_habit_create()
        resp = self.client.get(reverse('my_habit_list'), data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_habit_delete(self):
        self.test_habit_create()
        resp = self.client.delete(reverse('habit_delete', args=[2]))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_habit_update(self):
        self.test_habit_create()
        resp = self.client.put(reverse('habit_update', args=[3]))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)