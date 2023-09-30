from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.shop'

    def ready(self):
        import applications.shop.signals
