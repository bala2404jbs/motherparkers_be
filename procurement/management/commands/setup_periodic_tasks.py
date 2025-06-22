from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule

class Command(BaseCommand):
    help = 'Setup periodic tasks for commodity price fetching'

    def handle(self, *args, **options):
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='0',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*'
        )
        PeriodicTask.objects.get_or_create(
            crontab=schedule,
            name='Fetch commodity prices daily',
            task='procurement.tasks.fetch_commodity_prices_task'
        )
        self.stdout.write(self.style.SUCCESS('Periodic task created.'))