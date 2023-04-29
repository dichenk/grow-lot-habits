from rest_framework import serializers


class HabitValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        periodic_habit = value.get('periodic_habit')
        pleasure_habit = value.get('pleasure_habit')
        binded_habit = value.get('binded_habit')
        reward = value.get('reward')
        time_for_finishing = value.get('time_for_finishing')
        #
        # if periodic_habit is None or time_for_finishing is None :
        #     raise serializers.ValidationError('Обхекты не могут быть None')

        if binded_habit is not None and reward != '':
            raise serializers.ValidationError(
                'исключается одновременный выбор связанной привычки и указания вознаграждения')
        if periodic_habit > 7:
            raise serializers.ValidationError('периодичность не может быть более 7 дней, то есть привычку нельзя '
                                              'выполнять больше, чем раз в неделю')
        if time_for_finishing > 120:
            raise serializers.ValidationError('время выполнения должно быть не больше 120 секунд')
        if binded_habit == '' and reward == '':
            raise serializers.ValidationError(
                'нельзя, чтобы связанная привычка и вознаграждение были одновременно пустые')
        if binded_habit is not None and pleasure_habit is True:
            raise serializers.ValidationError(
                'в связанные привычки могут попадать только привычки с признаком приятной привычки')
        if pleasure_habit is True and (reward is not None or binded_habit is not None):
            raise serializers.ValidationError('у приятной привычки не может быть вознаграждения или связанной привычки')
