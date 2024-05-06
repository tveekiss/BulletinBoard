import logging
from datetime import timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.utils import timezone

from users.models import OneTimeCode


logger = logging.getLogger(__name__)


def delete_users():
    max_date = timezone.now() - timedelta(hours=24)
    delete_users = User.objects.filter(last_login=None, date_joined__lte=max_date)
    for user in delete_users:
        user.delete()
        logger.info(f"Delete {user.username}")
    logger.info(f"Deleted {len(delete_users)} users {timezone.now()}")


def delete_codes():
    max_date = timezone.now() - timedelta(minutes=5)
    delete_cods = OneTimeCode.objects.filter(created__lte=max_date)

    for code in delete_cods:
        code.delete()
        logger.info(f"Delete {code.code}")
    logger.info(f"Deleted {len(delete_cods)} codes {timezone.now()}")


# The `close_old_connections` decorator ensures that database connections,
# that have become unusable or are obsolete, are closed before and after your
# job has run. You should use it to wrap any jobs that you schedule that access
# the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age`
    from the database.
    It helps to prevent the database from filling up with old historical
    records that are no longer useful.

    :param max_age: The maximum length of time to retain historical
                    job execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            delete_codes,
            trigger=CronTrigger(minute="*/5"),  # Every 10 seconds
            id="delete-codes",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'delete_codes'.")

        scheduler.add_job(
            delete_users,
            trigger=CronTrigger(hour="12", minute="00"),
            id='delete-users',
            max_instances=1,
            replace_existing=True
        )
        logger.info("Added daily job: 'delete_users'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
