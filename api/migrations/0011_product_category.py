# Generated by Django 4.1 on 2023-04-20 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.IntegerField(default=4),
        ),
    ]