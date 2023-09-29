from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/shop/', include('applications.shop.urls'), name='shop'),
    path('api/v1/', include('applications.account.urls'), name='account'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)