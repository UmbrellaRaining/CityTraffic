# Generated by Django 5.0.1 on 2024-01-18 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0012_user_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='logo',
            field=models.ImageField(default='', max_length=90, upload_to=''),
        ),
    ]
