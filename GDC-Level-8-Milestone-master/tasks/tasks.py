import time
from datetime import datetime, timedelta

from celery.decorators import periodic_task
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from task_manager.celery import app
from task_manager.settings import EMAIL_HOST_USER

from .models import EmailReport, Task


@periodic_task(run_every=timedelta(minutes=1))
def send_email_remainder(*args, **kwargs):
    """
    send email report
    """
    current_time = datetime.now().strftime("%H:%M")
    current_time_1 = (datetime.now() - timedelta(minutes=1)).strftime("%H:%M")
    current_time = datetime.strptime(str(current_time), "%H:%M").time()
    current_time_1 = datetime.strptime(str(current_time_1), "%H:%M").time()

    print(current_time, current_time_1)
    
    # will select all emails that is to sent at current time
    # and in case of any past system failures some emails 
    # may not be sent they can be resend 
    # if they were not sent in the last 24 hours
    reports = EmailReport.objects.filter(
        Q(time__lte=current_time ,time__gte=current_time_1)
        | Q(last_sent__lte=timezone.now() - timedelta(hours=24))
    )
    print(reports)
    with transaction.atomic():
        for user in reports:
            report_content = f"Hi {user.user.username},\n\n"
            report_content += f"You have {Task.objects.filter(user=user.user).count()} tasks remaining.\n\n"
            report_content += "\n\nPending Tasks:\n"
            for task in Task.objects.filter(user=user.user, completed=False):
                report_content += f"{task.title}\n"
            report_content += "\n\nCompleted Tasks:\n"
            for task in Task.objects.filter(user=user.user, completed=True):
                report_content += f"{task.title}\n"
            report_content += "\n\nThank you!"
            # send_mail(
            #     "Task Manager Reminder",
            #     report_content,
            #     EMAIL_HOST_USER,
            #     [user.user.email],
            # )
            msg = EmailMessage(
                "Task Manager Reminder",
                report_content,
                EMAIL_HOST_USER,
                [user.user.email],
            )
            msg.send()
            user.last_sent = datetime.now(tz=timezone.utc)
            user.save()
            print("message_sent")
