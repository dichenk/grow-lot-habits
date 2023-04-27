import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util


logger = logging.getLogger(__name__)


def read_json(variable):  # json.loads не хочет читать одинарные кавычки и True. Поправим.
    variable = variable.replace("'", "\"")
    variable = variable.replace("True", "\"True\"")
    variable = variable.replace("False", "\"False\"")
    variable = json.loads(variable)
    return variable


def take_status(variable):
    status_request = {
        "TerminalKey": "1677659270153DEMO",
        "OrderId": None,
        "Token": None
    }
    order_id = variable['OrderId']
    status_request['OrderId'] = order_id
    str_to_token = status_request['OrderId'] + '9rgoqv88ygs8g7ed' + status_request['TerminalKey']
    request_hash = sha256(str_to_token.encode()).hexdigest()
    status_request['Token'] = request_hash
    status_answer = requests.post('https://securepay.tinkoff.ru/v2/CheckOrder', json.dumps(status_request))
    status_answer = read_json(status_answer.text)
    status_answer = status_answer["Payments"][0]['Status']
    return status_answer


def my_job():
    # models = Payment
    payment_object = list(Payment.objects.all())
    #  запрос, чтобы узнать статус оплаты https://www.tinkoff.ru/kassa/develop/api/payments/checkorder-description/
    i = -1
    while 1:
        try:  # объект Payment is not iterable ¯\_(ツ)_/¯
            i += 1
            if payment_object[i].result_payment == 'success':  # проверяем только записи с неоплаченными заказами:
                continue
            variable = payment_object[i].response_payment  # хотим достать номер заказа, чтобы чекнуть оплату
            variable = read_json(variable)
            if variable['ErrorCode'] == '0':  # цель - достать статус оплаты
                variable = take_status(variable)
            else:
                continue
            if variable == 'CONFIRMED':  # если пользователь оплатил заказ по ссылке - меняем статус в базе и больше его не проверяем
                success_order = Payment.objects.get(pk=payment_object[i].pk)
                success_order.result_payment = 'success'
                success_order.save()
        except:
            break


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # Every 60 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
