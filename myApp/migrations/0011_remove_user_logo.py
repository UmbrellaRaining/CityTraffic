# Generated by Django 5.0.1 on 2024-01-18 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0010_user_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='logo',
        ),
    ]
