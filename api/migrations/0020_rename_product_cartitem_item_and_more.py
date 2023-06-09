# Generated by Django 4.1 on 2023-04-25 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_cart_items'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='product',
            new_name='item',
        ),
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('cart', 'item', 'quantity')},
        ),
    ]
