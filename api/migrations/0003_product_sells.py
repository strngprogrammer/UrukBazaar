# Generated by Django 4.1 on 2023-04-18 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sells',
            field=models.IntegerField(default=0),
        ),
    ]
