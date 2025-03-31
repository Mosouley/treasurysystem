from django.urls import path, include
from rest_framework import routers
from contacts import views


router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet)
router.register(r'accounts', views.AccountViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet)


urlpatterns = []
urlpatterns += router.urls