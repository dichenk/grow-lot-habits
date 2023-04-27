from app_habit.views import HabitCreateView, HabitListView
from django.urls import path


urlpatterns = [
        path('', HabitListView.as_view(), name='habit_list'),
        path('create/', HabitCreateView.as_view(), name='habit_create'),
        # path('lesson/delete/<int:pk>/', LessonDeleteView.as_view(), name='lesson_delete'),
        # path('course/<int:pk>/', CourseSingleView.as_view()),
        # path('course/', CourseListView.as_view(), name='course_list'),
        # path('course/create/', CourseCreateView.as_view(), name='course_create'),
        # path('course/delete/<int:pk>/', CourseDeleteView.as_view(), name='course_delete'),
        # path('subscription/create/', SubscriptionCreateView.as_view(), name='subscription_create'),
        # path('subscription/', SubscriptionListView.as_view()),
        # path('subscription/delete/<int:pk>/', SubscriptionDeleteView.as_view()),
        # path('payment/create/', PaymentCreateView.as_view()),
        # path('payment/<int:pk>/', PaymentSingleView.as_view()),
        # path('payment/update/<int:pk>/', PaymentUpdateView.as_view()),
]
