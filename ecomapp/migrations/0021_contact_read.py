# Generated by Django 5.1.2 on 2024-11-05 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0020_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
