from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

# class Token(models.Model):
#     key = models.CharField(max_length=40, primary_key=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='auth_token', on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = _('Token')
#         verbose_name_plural = _('Tokens')

#     def __str__(self):
#         return self.key

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='api/products/', blank=True)
    sells = models.IntegerField(default=0)
    category = models.IntegerField()

    def __str__(self):
        return self.name
    
class Categories(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='api/categories/', blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'item', 'quantity')