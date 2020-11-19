# Generated by Django 3.1.3 on 2020-11-19 17:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20201116_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='pages_num',
            field=models.PositiveIntegerField(blank=True, default=1, help_text='Number of pages', null=True, validators=[django.core.validators.MaxValueValidator(9999)]),
        ),
    ]
