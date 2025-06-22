from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField

# ----------------------
# Module 1: Market & Commodity Intelligence
# ----------------------
class Commodity(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    unit_of_measure = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class CommodityPrice(models.Model):
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=12, decimal_places=4)
    source_api = models.CharField(max_length=100)
    currency = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.commodity.name} - {self.date}"

class PricePrediction(models.Model):
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    prediction_date = models.DateField()
    predicted_price = models.DecimalField(max_digits=12, decimal_places=4)
    model_version = models.CharField(max_length=50)
    confidence_score = models.FloatField()
    def __str__(self):
        return f"{self.commodity.name} - {self.prediction_date}"

class CommodityNews(models.Model):
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    article_data = JSONField()  # Stores article {'id': index}
    fetch_date = JSONField(null=True)  # Temporary nullable
    time_range_start = JSONField(null=True)  # Temporary nullable
    time_range_end = JSONField(null=True)  # Temporary nullable
    
    # Search term fields
    coffee_commodity_price_fluctuation = JSONField(default=list)
    coffee_geopolitical_tensions = JSONField(default=list)
    coffee_logistics_delays = JSONField(default=list)
    coffee_shipping_costs = JSONField(default=list)
    coffee_freight_rates = JSONField(default=list)
    coffee_natural_disasters = JSONField(default=list)
    coffee_labor_strikes = JSONField(default=list)
    coffee_market_shortage = JSONField(default=list)
    coffee_procurement_fraud = JSONField(default=list)
    coffee_supplier_risk = JSONField(default=list)
    coffee_global_demand_shift = JSONField(default=list)
    coffee_manufacturing_slowdown = JSONField(default=list)
    coffee_regulatory_changes = JSONField(default=list)

    def __str__(self):
        return f"{self.commodity.name} - News"

    class Meta:
        indexes = [
            models.Index(fields=['commodity']),
        ]

class ProcurementNewsSummary(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    result_json = JSONField()

    class Meta:
        ordering = ['-created_at']  # Latest first
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Summary {self.created_at}"


# ----------------------
# Module 2: Supply Chain Risk Management
# ----------------------
class SourcingRegion(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    geo_coordinates = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}, {self.country}"

class RiskType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.name

class RiskEvent(models.Model):
    region = models.ForeignKey(SourcingRegion, on_delete=models.CASCADE)
    risk_type = models.ForeignKey(RiskType, on_delete=models.CASCADE)
    description = models.TextField()
    severity = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    event_date = models.DateField()
    source_data = models.TextField()
    impacted_commodities = models.ManyToManyField(Commodity, blank=True)
    def __str__(self):
        return f"{self.risk_type.name} in {self.region.name} on {self.event_date}"

class SupplierRiskScore(models.Model):
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    score_date = models.DateField()
    overall_score = models.FloatField()
    geopolitical_score = models.FloatField()
    climate_score = models.FloatField()
    status = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.supplier.name} - {self.score_date}"

# ----------------------
# Module 3: Sustainability & Ethical Sourcing Compliance
# ----------------------
class Certification(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    issuing_body = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class SupplierCertification(models.Model):
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE)
    date_obtained = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.supplier.name} - {self.certification.name}"

class SustainabilityMetric(models.Model):
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    metric_type = models.CharField(max_length=100)
    value = models.FloatField()
    date = models.DateField()
    source = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.supplier.name} - {self.metric_type}"

class AuditReport(models.Model):
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    audit_date = models.DateField()
    report_summary = models.TextField()
    compliance_status = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.supplier.name} - {self.audit_date}"

# ----------------------
# Module 4: Demand & Inventory Optimization
# ----------------------
class RawMaterial(models.Model):
    name = models.CharField(max_length=100)
    unit_of_measure = models.CharField(max_length=50)
    min_stock_level = models.FloatField()
    max_stock_level = models.FloatField()
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50)
    unit_of_sale = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class ProductComponent(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity_needed = models.FloatField()
    def __str__(self):
        return f"{self.product.name} - {self.raw_material.name}"

class SalesData(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    quantity_sold = models.FloatField()
    def __str__(self):
        return f"{self.product.name} - {self.date}"

class MaterialForecast(models.Model):
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    forecast_date = models.DateField()
    predicted_demand_qty = models.FloatField()
    model_version = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.raw_material.name} - {self.forecast_date}"

class InventoryLevel(models.Model):
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    warehouse = models.CharField(max_length=100)
    quantity = models.FloatField()
    last_updated = models.DateTimeField()
    def __str__(self):
        return f"{self.raw_material.name} - {self.warehouse}"

# ----------------------
# Module 5: Supplier Performance & Relationship Management (SRM)
# ----------------------
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    address = models.TextField()
    primary_commodity = models.ForeignKey(Commodity, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.name

class SupplierEvaluationMetric(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.name

class SupplierPerformance(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    metric = models.ForeignKey(SupplierEvaluationMetric, on_delete=models.CASCADE)
    score = models.FloatField()
    date = models.DateField()
    notes = models.TextField(blank=True)
    def __str__(self):
        return f"{self.supplier.name} - {self.metric.name} - {self.date}"

class SupplierInteraction(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=100)
    date = models.DateField()
    summary = models.TextField()
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"{self.supplier.name} - {self.interaction_type} - {self.date}"

# ----------------------
# Module 6: Spend Analytics & Cost Optimization
# ----------------------
class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    order_date = models.DateField()
    status = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)
    def __str__(self):
        return self.po_number

class PurchaseOrderItem(models.Model):
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)
    def __str__(self):
        return f"{self.po.po_number} - {self.raw_material.name}"

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.name

class SpendTransaction(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_date = models.DateField()
    description = models.TextField(blank=True)
    invoice_number = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return f"{self.supplier.name} - {self.amount} - {self.transaction_date}"

# ----------------------
# Module 7: Automated Procurement Operations
# ----------------------
class Invoice(models.Model):
    invoice_number = models.CharField(max_length=100, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=50)
    def __str__(self):
        return self.invoice_number
