from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ProcurementNewsAnalysisView,CommodityNewsByUUIDView

router = DefaultRouter()
router.register(r'commodities', views.CommodityViewSet)
router.register(r'commodity-prices', views.CommodityPriceViewSet)
router.register(r'price-predictions', views.PricePredictionViewSet)
# ... add more routers as views are implemented

urlpatterns = [
    path('', include(router.urls)),
    path('procurement-news-analysis/', ProcurementNewsAnalysisView.as_view(), name='procurement-news-analysis'),
    path('commodity-news/', CommodityNewsByUUIDView.as_view(), name='commodity-news-by-uuid'),
]
