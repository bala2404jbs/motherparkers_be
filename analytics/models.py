from django.db import models

class MLModel(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} v{self.version}"

class MLModelRun(models.Model):
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE)
    run_date = models.DateTimeField(auto_now_add=True)
    parameters = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=50)
    def __str__(self):
        return f"Run {self.id} for {self.model}"

class MLModelResult(models.Model):
    run = models.ForeignKey(MLModelRun, on_delete=models.CASCADE)
    result_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Result for Run {self.run.id}"
