from django.db import models


class Record(models.Model):
    time = models.DateTimeField(auto_now=True)
    price = models.FloatField()
