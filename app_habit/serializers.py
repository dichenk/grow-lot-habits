from rest_framework import serializers
from app_habit.models import Habit

from app_habit.validators import HabitValidator


# from rest_framework.fields import CurrentUserDefault
# import requests
#
#
class HabitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = (
            'time',
            'place',
            'action',
            'reward',
            'time_for_finishing',
        )
        validators = [HabitValidator(field='model')]


class HabitViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

#
# class PaymentMakeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = (
#             'user',
#             'course',
#             'response_payment',
#             'id',
#             'result_payment'
#         )
#
#
# class PaymentUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = (
#             'result_payment',
#         )
#
#
# class CourseSingleSerializer(serializers.ModelSerializer):
#     #    is_there_subscription = serializers.SerializerMethodField()
#     sub_status = SubscriptionListSerializer(source='course_subs', many=True)
#
#     #    paym_status = PaymentMakeSerializer(source='course_paym', many=True)
#     class Meta:
#         model = Course
#         fields = ('title',
#                   #                  'is_there_subscription',
#                   'sub_status'
#                   #                 'paym_status',
#                   )
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         if representation['sub_status']:
#             representation['sub_status'] = 'Вы подписаны на курс'
#         else:
#             representation['sub_status'] = 'Вы не подписаны на этот курс'
#         # if representation['paym_status'] == 'failure':
#         #     representation['paym_status'] = 'Купите курс!'
#         # else:
#         #     representation['paym_status'] = 'Вы приобрели этот курс!'
#         return representation
#
#     '''хахаха, накопал, как зацепить реквест юзера в сериалайзере, а оно не понадобилось
#     оставлю как памятник
#     def get_is_there_subscription(self, instance):
#         request_user = self.context.get("request").user.id
#         return 5'''
#
#
# class PaymentSingleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = (
#             'date_of_payment',
#             'course',
#             'result_payment'
#         )
#
#
# class LessonCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Lesson
#         fields = (
#             'course',
#             'title',
#             'description',
#             'video_link',
#         )
#         validators = [LessonValidator(field='model')]
#
#
# class CourseViewSerializer(serializers.ModelSerializer):
#     amount_of_lessons = serializers.SerializerMethodField()
#     lessons = LessonViewSerializer(source='courses', many=True)
#
#     class Meta:
#         model = Course
#         fields = (
#             'id',
#             'title',
#             'description',
#             'preview',
#             'amount_of_lessons',
#             'lessons',
#             'author',
#         )
#
#     def get_amount_of_lessons(self, instance):
#         return Lesson.objects.filter(course=instance).count()
#
#
# class LessonDeleteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Lesson
#         fields = ('id')
#
#
# class CourseDeleteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Course
#         fields = ('id')
#
#
# class CourseCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Course
#         fields = (
#             'title',
#             'description',
#         )
#
#
# class SubscriptionCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subscription
#         fields = (
#             'user',
#             'course',
#         )
#
#
# class SubscriptionDeleteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subscription
#         fields = ('id',)
