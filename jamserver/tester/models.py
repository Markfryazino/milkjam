from django.db import models

run_fields = ['name', 'comment', 'start_balance']


class Run(models.Model):
    name = models.TextField(unique=True)
    start_time = models.DateTimeField(auto_now=True)
    comment = models.TextField(default="no comments")
    start_balance = models.FloatField(default=200.)
    duration = models.FloatField(null=True)


class Snapshot(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    usd_balance = models.FloatField()
    btc_balance = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)
