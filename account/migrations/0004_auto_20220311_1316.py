# Generated by Django 3.2 on 2022-03-11 13:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='groups', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='updated',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_group', to=settings.AUTH_USER_MODEL),
        ),
    ]
