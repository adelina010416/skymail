from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJob

from mailing.models import Mail
from mailing.services import start_scheduler

scheduler_test = BlockingScheduler()
scheduler_test.add_jobstore(DjangoJobStore(), "default")


class Command(BaseCommand):
    help = 'Runs the APScheduler'

    def handle(self, *args, **options):
        email = input('Введите почту получателя: ')
        mail_id = input('Введите id рассылки, которую хотите запустить: ')

        try:
            DjangoJob.objects.filter(id=mail_id + 'admin').delete()
        except JobLookupError:
            pass
        mail = Mail.objects.get(id=int(mail_id))
        start_scheduler(mail, [email], 'admin', scheduler_test)
        print('Рассылка запущена')
        scheduler_test.start()
