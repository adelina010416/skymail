from apscheduler.schedulers import SchedulerAlreadyRunningError
from django.core.mail import send_mail

from config import settings
from config.urls import scheduler


def do_mailing(mail, clients):
    send_mail(
        subject=mail.message.header,
        message=mail.message.body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=clients
    )


def start_scheduler(mail, clients, user_pwd):
    if mail.frequency == 'daily':
        scheduler.add_job(do_mailing, 'interval', id=str(mail.id)+str(user_pwd), start_date=mail.start_time,
                          day=1, args=[mail, clients])
    elif mail.frequency == 'weekly':
        scheduler.add_job(do_mailing, 'interval', id=str(mail.id)+str(user_pwd), start_date=mail.start_time,
                          day=7, args=[mail, clients])
    else:
        scheduler.add_job(do_mailing, 'cron', id=str(mail.id)+str(user_pwd), day=mail.start_time.day, hour=mail.start_time.hour,
                          minute=mail.start_time.minute, second=mail.start_time.second,
                          start_date=mail.start_time, weeks=1, args=[mail, clients])
    try:
        scheduler.start()
    except SchedulerAlreadyRunningError:
        pass
