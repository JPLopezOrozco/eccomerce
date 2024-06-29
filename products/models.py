from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


class Product(models.Model):
    GENDER_CHOICES = [
        ('U','Unisex'),
        ('M', 'Men'),
        ('W', 'Women'),
    ]
    BRAND_CHOICES = [
        ('NIKE','Nike'),
        ('ADIDAS','Adidas'),
        ('PUMA','Puma'),
        ('UNDER_ARMOUR','Under armour'),
        ('NEW_BALANCE','New Balance'),
    ]
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, choices=BRAND_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    image = models.ImageField(upload_to='products/products_images')
    
    def __str__(self):
        return f"{self.name}, id:{self.id}"

    
    
class ProductSize(models.Model):
    product = models.ForeignKey(Product, related_name='sizes', on_delete=models.CASCADE)
    size = models.DecimalField(validators=[MinValueValidator(7), MaxValueValidator(15)], max_digits=10, decimal_places=1)
    quantity = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['size']
    
    def __str__(self):
        return f"{self.product.name} - size {self.size}"
    
class Review(models.Model):
    SCORE_CHOICES = [
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
        (6,'6'),
        (7,'7'),
        (8,'8'),
        (9,'9'),
        (10,'10'),

    ]
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comments = models.TextField(max_length=255)
    score = models.IntegerField(choices=SCORE_CHOICES)
    
    
    def __str__(self) -> str:
        return f'{self.created_by}, {self.product.name}, {self.score}'