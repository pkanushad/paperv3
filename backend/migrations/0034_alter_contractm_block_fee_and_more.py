# Generated by Django 4.1.5 on 2023-04-12 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0033_futureblottermodel_physica_blotter_connect_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractm',
            name='block_fee',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contractm',
            name='exchange_fee',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contractm',
            name='exchanging_clearing_fee',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contractm',
            name='screen_fee',
            field=models.TextField(blank=True, null=True),
        ),
    ]
