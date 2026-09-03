from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class PregnancyWeek(models.Model):

    week_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return f"Week {self.week_number} - {self.title}"