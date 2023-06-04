# Generated by Django 4.1 on 2023-04-25 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_remove_cart_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(related_name='carts', through='api.CartItem', to='api.product'),
        ),
    ]