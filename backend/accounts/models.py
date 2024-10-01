from django.db import models

from django.utils import timezone
# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    archive = models.BooleanField(default=False)
    trash = models.BooleanField(default=False)
    pin = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'
