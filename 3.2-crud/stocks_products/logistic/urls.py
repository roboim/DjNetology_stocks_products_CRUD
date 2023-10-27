from rest_framework.routers import DefaultRouter
from django.urls import path

from logistic.views import ProductViewSet, StockViewSet

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('stocks', StockViewSet)

urlpatterns = router.urls
# urlpatterns = urlpatterns + [
#     path('products/<int:pk>/', SensorIdView.as_view()),
# ]