# Generated by Django 4.1.5 on 2023-04-04 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0023_alter_physicalblottermodel_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='physicalblottermodel',
            name='bl_date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
