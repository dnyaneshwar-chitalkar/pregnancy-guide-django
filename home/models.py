from django.db import models

class PregnancyWeek(models.Model):
    week_number =models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()


    def __str__(self):
        return  f"Week {self.week_number}  - {self.title}"