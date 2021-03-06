# Generated by Django 3.2 on 2022-03-11 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20220311_1422'),
        ('connection', '0004_alter_joinrequest_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectionRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent', models.DateTimeField(auto_now_add=True)),
                ('dest_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_request', to='account.group')),
                ('source_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_request', to='account.group')),
            ],
            options={
                'ordering': ('-sent',),
            },
        ),
    ]
