# Generated by Django 3.1 on 2020-08-26 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacatcher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='run_id',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
    ]
