# Generated by Django 4.1.5 on 2023-05-08 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0042_alter_brockeragem_options_alter_clearerratem_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='swapblottermodel',
            name='total_n_days',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
