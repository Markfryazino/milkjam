# Generated by Django 3.1 on 2020-09-03 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacatcher', '0003_auto_20200830_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='asks',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='record',
            name='bids',
            field=models.TextField(null=True),
        ),
    ]
