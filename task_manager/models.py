from django.db import models

from bars import settings
from account.models import *
import datetime

from bp_manager.models import Process


class Task(models.Model):
    OPEN = 'OPEN'
    IN_PROGRESS = 'IN_P'
    FINISHED = 'FIN'
    STATUS_CHOICES = (
        (OPEN, 'Open'),
        (IN_PROGRESS, 'In progress'),
        (FINISHED, 'Finished'),
    )
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=4096)
    executor = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='Executor', null=True,
                                    blank=True)
    role = models.CharField(max_length=4, choices=CustomUser.ROLE_CHOICES)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default=OPEN)
    process = models.ForeignKey(Process, on_delete=models.CASCADE, null=True)
    deadline = models.DateTimeField(default=datetime.datetime.now())
