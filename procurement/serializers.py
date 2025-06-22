from rest_framework import serializers
from .models import *

# Commodity, CommodityPrice, PricePrediction, SourcingRegion, RiskType, RiskEvent, SupplierRiskScore, Certification, SupplierCertification, SustainabilityMetric, AuditReport, RawMaterial, Product, ProductComponent, SalesData, MaterialForecast, InventoryLevel, Supplier, SupplierEvaluationMetric, SupplierPerformance, SupplierInteraction, PurchaseOrder, PurchaseOrderItem, ExpenseCategory, SpendTransaction, Invoice

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = '__all__'

class CommodityPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommodityPrice
        fields = '__all__'

class PricePredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricePrediction
        fields = '__all__'

class CommodityNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommodityNews
        fields = [
            'id', 'commodity', 'article_data', 'fetch_date', 'time_range_start', 'time_range_end',
            'coffee_commodity_price_fluctuation', 'coffee_geopolitical_tensions', 'coffee_logistics_delays',
            'coffee_shipping_costs', 'coffee_freight_rates', 'coffee_natural_disasters', 'coffee_labor_strikes',
            'coffee_market_shortage', 'coffee_procurement_fraud', 'coffee_supplier_risk',
            'coffee_global_demand_shift', 'coffee_manufacturing_slowdown', 'coffee_regulatory_changes'
        ]

# ... More serializers will be added as models are implemented
