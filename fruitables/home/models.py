from django.db import models
from django.conf import settings
from django.utils.text import slugify
from decimal import Decimal, ROUND_HALF_UP


class Category(models.Model):
    category_name = models.CharField(max_length=255, verbose_name="Category")
    slug = models.SlugField(blank=True, unique=True)
    photo = models.ImageField(upload_to='images/categories/%Y/%m/%d/', blank= True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)
    
    
    def __str__(self) -> str:
        return self.category_name
    
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=255, verbose_name="Product")
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(verbose_name="Discount", blank=True, null=True)
    photo = models.ImageField(upload_to='images/products/%Y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, 
                                      verbose_name="Created at"
                                      )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Updated at")
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.product_name


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.product_name} for {self.user}'

    def get_total_price(self):
        if self.product.discount:
            price = Decimal(self.product.price)
            discount = Decimal(self.product.discount)
            total_price = (price-price * (discount/Decimal(100))) * self.quantity
            print("TOTAL PRICE : ", total_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
            return total_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return self.product.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_status = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Order {self.id} by {self.user.username}'
    
    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, 'Unknown')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} of {self.product.name} in Order {self.order.id}'

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.quantity} x {self.product.product_name} in Order {self.order.id}'