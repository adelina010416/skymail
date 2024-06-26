import smtplib
from datetime import datetime

from django.core.mail import send_mail

from attempt_report.models import Attempt
from config import settings


def do_mailing(mail, user):
    clients_list = []
    recipients = mail.recipients.all()
    [clients_list.append(client.email) for client in recipients]
    try:
        server_response = send_mail(
            subject=mail.message.header,
            message=mail.message.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=clients_list,
            fail_silently=False
        )
        Attempt.objects.create(mail=mail,
                               user=user,
                               date_time=datetime.now(),
                               status='successful',
                               mail_server_response=server_response)
    except smtplib.SMTPException as e:
        Attempt.objects.create(mail=mail,
                               user=user,
                               date_time=datetime.now(),
                               status='unsuccessful',
                               mail_server_response=e)


def start_scheduler(mail, user, scheduler):
    if mail.frequency == 'daily':
        scheduler.add_job(do_mailing, 'interval', id=str(mail.id) + str(user.verified_password),
                          start_date=mail.start_time,
                          days=1, args=[mail, user])
    elif mail.frequency == 'weekly':
        scheduler.add_job(do_mailing, 'interval', id=str(mail.id) + str(user.verified_password),
                          start_date=mail.start_time,
                          days=7, args=[mail, user])
    else:
        scheduler.add_job(do_mailing, 'cron', id=str(mail.id) + str(user.verified_password),
                          day=mail.start_time.day,
                          hour=mail.start_time.hour,
                          minute=mail.start_time.minute,
                          second=mail.start_time.second,
                          start_date=mail.start_time,
                          timezone='utc',
                          args=[mail, user])
