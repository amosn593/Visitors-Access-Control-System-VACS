# Generated by Django 3.2.5 on 2021-10-15 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitor', '0005_auto_20211015_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='vehicle_occupants',
            field=models.CharField(default=0, max_length=20, null=True),
        ),
    ]
