from django.db import models

# Create your models here.
from django.db import models


class Prediction(models.Model):
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    bmi = models.FloatField()
    children = models.IntegerField()
    smoker = models.CharField(max_length=10)
    region = models.CharField(max_length=20)

    predicted_charge = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.age} - {self.predicted_charge}"