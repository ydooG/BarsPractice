from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from account.managers import CustomUserManager
from vcs.models import Repository


class CustomUser(AbstractUser):
    MANAGER = 'MAN'
    ANALYST = 'AN'
    DEVELOPER = 'DEV'
    TESTER = 'TEST'
    ROLE_CHOICES = (
        (MANAGER, 'Manager'),
        (ANALYST, 'Analyst'),
        (DEVELOPER, 'Developer'),
        (TESTER, 'Tester'),
    )
    username = models.CharField(max_length=30,
                                verbose_name='Login',
                                unique=True)
    role = models.CharField(max_length=4,
                            choices=ROLE_CHOICES, )
    room = models.ForeignKey('Room',
                             on_delete=models.SET_NULL,
                             related_name='users',
                             related_query_name='users',
                             null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def set_position(self, pos):
        self.role = pos

    def is_manager(self):
        return self.role == self.MANAGER


class Room(models.Model):
    title = models.CharField(max_length=50)
    repository = models.OneToOneField(Repository,
                                      related_name='room',
                                      on_delete=models.SET_NULL,
                                      blank=True,
                                      null=True)

    author = models.OneToOneField(CustomUser,
                                  on_delete=models.CASCADE,
                                  related_name='my_room',
                                  related_query_name='my_room')

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('music:singer_detail', args=[self.id, ])
