from django.db import models

class Mqtt(models.Model):
    T = models.CharField(max_length=10)
    H = models.CharField(max_length=10)
    status = models.CharField(max_length=10)