# Generated by Django 3.2 on 2022-03-11 15:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('connection', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joinrequest',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='join_request', to=settings.AUTH_USER_MODEL),
        ),
    ]
