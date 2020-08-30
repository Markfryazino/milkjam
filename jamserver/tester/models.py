from django.db import models
from datacatcher.models import Record

run_fields = ['name', 'comment', 'start_balance', 'start_time']


class Run(models.Model):
    name = models.TextField(unique=True)
    start_time = models.DateTimeField()
    comment = models.TextField(default="no comments")
    start_balance = models.FloatField(default=200.)
    duration = models.FloatField(null=True)


class Snapshot(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    balances = models.TextField(null=True)
    usd_balance = models.FloatField(null=True)
    timestamp = models.DateTimeField()
    record = models.ForeignKey(Record, on_delete=models.CASCADE, null=True)
