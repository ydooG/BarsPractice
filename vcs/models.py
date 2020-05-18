from django.db import models
from django.urls import reverse


class Repository(models.Model):
    name = models.CharField(max_length=128)
    url = models.URLField()

    def get_absolute_url(self):
        return reverse('vcs')