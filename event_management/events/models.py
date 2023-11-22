from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# here need to create the models like -> customuser,events,notifications;

class CustomUser(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=10, unique=True)
    email_id = models.EmailField(unique=True)
    address = models.TextField(null=False, blank=False, max_length=50)

    def __str__(self):
        return self.username


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20, null=False, blank=False)
    description = models.TextField(max_length=255, blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='organized_events')

    def __str__(self):
        return self.title


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message}"
