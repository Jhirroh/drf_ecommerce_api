from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from .signals import create_transaction_id


class TimeStampModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name


class Product(TimeStampModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=6)
    stock = models.IntegerField()
    image_url = models.ImageField(upload_to='products/')

    def __str__(self) -> str:
        return self.name


class OrderItem(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Order Items'

    def __str__(self) -> str:
        return f'{self.quantity} of {self.product.name}'

    def get_total_item_price(self) -> int:
        return self.quantity * self.product.price


class ShippingAddress(TimeStampModel):
    SHIPPING_TYPES = (
        ('HOME', 'Home'),
        ('OFFICE', 'Office'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=255, choices=SHIPPING_TYPES)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Shipping Addresses'

    def __str__(self) -> str:
        return self.address


class Order(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    transaction_id = models.CharField(max_length=10)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)
    date_delivered = models.DateTimeField(null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    date_cancelled = models.DateTimeField(null=True, blank=True)
    is_cancelled = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.transaction_id

    def get_total_price(self) -> int:
        total_price = 0
        for item in self.items.all():
            total = item.get_total_item_price()
            total_price += total
        return total_price


post_save.connect(create_transaction_id, sender=Order)
