# Generated by Django 3.1.3 on 2020-11-11 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20201111_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='slug',
            field=models.SlugField(blank=True, max_length=300),
        ),
    ]
