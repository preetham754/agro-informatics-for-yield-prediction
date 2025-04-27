from django.db import models
from django.contrib.auth.models import User

class Crop(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Season(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=2)

    def __str__(self):
        return self.name

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    area = models.FloatField()
    production = models.FloatField()
    annual_rainfall = models.FloatField()
    fertilizer = models.FloatField()
    pesticide = models.FloatField()
    predicted_yield = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop.name} - {self.predicted_yield} t/ha"