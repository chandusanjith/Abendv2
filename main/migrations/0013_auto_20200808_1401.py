# Generated by Django 3.0.7 on 2020-08-08 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0012_auto_20200808_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorials',
            name='tags',
            field=models.ManyToManyField(related_name='tag_tutorial_master', to='test1.Tags'),
        ),
    ]
