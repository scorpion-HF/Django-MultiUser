# Generated by Django 4.2 on 2023-10-09 16:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_normalprofile_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='normalprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='normal_profile', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='supervisorprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='supervisor_profile', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
