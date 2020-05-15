from django.db import models

from account.models import Room, CustomUser


class Board(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, default='Board')


class Process(models.Model):
    ANALYZED = 'AN'
    IN_DEVELOPING = 'IN_D'
    TESTING = 'TEST'
    CHECKING = 'CHECK'
    FINISHED = 'FIN'
    STATUS_CHOICES = (
        (ANALYZED, 'Analyzed'),
        (IN_DEVELOPING, 'In developing'),
        (TESTING, 'Testing'),
        (CHECKING, 'Checking'),
        (FINISHED, 'Finished'),
    )
    name = models.CharField(max_length=64)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)


class Team(models.Model):
    # Тут я не знаю что писать, так что пока будет так.
    name = models.CharField(max_length=50, default='Team')
    managers = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='managers', null=True)
    workers = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)
