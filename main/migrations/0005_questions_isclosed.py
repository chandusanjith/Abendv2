# Generated by Django 3.0.7 on 2020-07-15 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0004_badges_badges_master_reputation'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='isclosed',
            field=models.BooleanField(default=False),
        ),
    ]
