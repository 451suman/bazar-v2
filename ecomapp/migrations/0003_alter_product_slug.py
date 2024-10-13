# Generated by Django 5.1.2 on 2024-10-13 08:35

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0002_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True),
        ),
    ]
