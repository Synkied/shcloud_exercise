# Generated by Django 3.2 on 2021-04-29 15:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='localization',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='resource',
                to='resources.localization'
            ),
        ),
        migrations.AlterField(
            model_name='resource',
            name='resource_type',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='resource',
                to='resources.resourcetype',
                verbose_name='resource type'
            ),
        ),
    ]
