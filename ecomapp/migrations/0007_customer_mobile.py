# Generated by Django 5.1.2 on 2024-10-14 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0006_alter_category_title_alter_customer_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='mobile',
            field=models.CharField(default=9856321470, max_length=10),
            preserve_default=False,
        ),
    ]
