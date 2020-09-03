from django.db import models


class Record(models.Model):
    timestamp = models.DateTimeField(auto_now=True, db_index=True)
    price = models.FloatField()
    run_id = models.IntegerField()
    asks = models.TextField(null=True)
    bids = models.TextField(null=True)
