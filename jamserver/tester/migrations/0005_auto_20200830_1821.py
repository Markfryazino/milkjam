# Generated by Django 3.1 on 2020-08-30 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tester', '0004_auto_20200830_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='last_action',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='run',
            name='start_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='snapshot',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
