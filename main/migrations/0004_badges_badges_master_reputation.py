# Generated by Django 3.0.7 on 2020-07-13 08:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('test1', '0003_notifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badges_Master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Badge_name', models.CharField(default='', max_length=200)),
                ('Rep_required', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Reputation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reputation_count', models.IntegerField(default=0)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('Rep_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Reputation_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Badges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('Badges_earned', models.ManyToManyField(related_name='Badges_users', to='test1.Badges_Master')),
                ('Badges_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Badges_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
