import pytz
from django.contrib.auth.models import User
from django.core.signals import request_finished
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("IN_PROGRESS", "IN_PROGRESS"),
    ("COMPLETED", "COMPLETED"),
    ("CANCELLED", "CANCELLED"),
)

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    priority = models.IntegerField()
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0]
    )

    def __str__(self):
        return self.title


class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    updated_date = models.DateTimeField(auto_now=True)
    new_status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0]
    )
    old_status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0]
    )

    def __str__(self):
        return self.task.title + "changed"

    # @classmethod
    # def create_history(cls, task):
    #     cls.objects.create(
    #         task=task, old_status=task.status, new_status=task.status
    #     ) if not task.status == task.previous_status else None


@receiver(pre_save, sender=Task)
def update_history(sender, instance, **kwargs):
    try:
        task = Task.objects.get(id=instance.id)
        if not task.status == instance.status:
            TaskHistory.objects.create(
                task=instance,
                old_status=task.status,
                new_status=instance.status,
            ).save()
            print("[hist]Task history created/updated")
    except Task.DoesNotExist:
        print("[hist]Task does not exist")
        pass


# request_finished.connect(update_history, dispatch_uid="update_history")


class EmailReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.TimeField(null=True, blank=True, default=timezone.now)
    time_zone = models.CharField(max_length=100)

