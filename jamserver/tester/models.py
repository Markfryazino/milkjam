from django.db import models
from datacatcher.models import Record

run_fields = ['name', 'comment', 'start_balance', 'start_time']


class Run(models.Model):
    name = models.TextField(unique=True)
    start_time = models.DateTimeField()
    comment = models.TextField(default="no comments")
    start_balance = models.FloatField(default=200.)
    duration = models.DurationField(null=True)
    end_balances = models.TextField(null=True)
    end_usdt = models.FloatField(null=True)


class Snapshot(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    balances = models.TextField(null=True)
    usd_balance = models.FloatField(null=True)
    timestamp = models.DateTimeField()
    record = models.ForeignKey(Record, on_delete=models.CASCADE, null=True)


class Action(models.Model):
    snapshot = models.ForeignKey(Snapshot, on_delete=models.CASCADE)
    query = models.TextField()
    delta = models.TextField()
