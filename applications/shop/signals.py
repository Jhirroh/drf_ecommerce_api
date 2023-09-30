import random
import string

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order


@receiver(post_save, sender=Order)
def create_transaction_id(sender, instance, created, **kwargs):
    if created:
        instance.transaction_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        instance.save()
