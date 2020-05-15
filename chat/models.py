from django.db import models
# ToDo: заменить импорт User на модель CustomUser из приложения Вероники
from account.models import CustomUser


class Chat(models.Model):
    name = models.CharField(max_length=64)
    members = models.ManyToManyField(CustomUser)

    def __str__(self):
        return self.name


class MessageContent(models.Model):
    text = models.TextField(max_length=4096)

    def __str__(self):
        return self.text


class Message(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.OneToOneField(MessageContent, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pub_date) + "|" + self.author.first_name + self.content.text


class Attachment(models.Model):
    CHOICES = (
        ("DOC", "Document"),
        ("IMG", "Image")
    )

    type = models.CharField(choices=CHOICES, max_length=50)
    messageContent = models.ForeignKey(MessageContent, on_delete=models.CASCADE)
    file = models.FileField(upload_to='messenger/attachments')
