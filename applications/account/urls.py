from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProfileViewSet, SignUpAPIView, LoginAPIView, LogoutAPIView

router = DefaultRouter()
router.register('profile/', ProfileViewSet, basename='profile')

urlpatterns = [
    path('signup/', SignUpAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
]
urlpatterns += router.urls
