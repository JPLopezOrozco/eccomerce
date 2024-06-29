from django.db import models
from products.models import ProductSize
from users.models import User
from order.models import Order, OrderItem


class CartUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True,)
    products = models.ManyToManyField(ProductSize, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,editable=False, default=0.00)

    def __str__(self) -> str:
        return f'ID:{self.id}, User:{self.user.username}, ${self.total}'

class CartItem(models.Model):
    product = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    cart = models.ForeignKey(CartUser,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('product', 'cart')

