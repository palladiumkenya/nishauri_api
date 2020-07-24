from django.db import models
from authApp.models import User, Dependants


class VLResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    r_id = models.CharField(max_length=50)
    result_type = models.CharField(max_length=10)
    result_content = models.CharField(max_length=30)
    date_collected = models.DateField()
    date_sent = models.DateTimeField(null=True)
    lab_name = models.CharField(max_length=150, null=True)

    class Meta:
        db_table = "VLResults"


class EidResults(models.Model):
    dependant = models.ForeignKey(Dependants, on_delete=models.CASCADE)
    r_id = models.CharField(max_length=50)
    result_type = models.CharField(max_length=10)
    result_content = models.CharField(max_length=30)
    date_collected = models.DateField()
    lab_name = models.CharField(max_length=150, null=True)

    class Meta:
        db_table = "EidResults"
