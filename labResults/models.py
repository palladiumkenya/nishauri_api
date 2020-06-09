from django.db import models
from authApp.models import User


class LabResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    r_id = models.CharField(max_length=50)
    result_type = models.CharField(max_length=10)
    result_content = models.CharField(max_length=30)
    date_collected = models.DateField()
    lab_name = models.CharField(max_length=150)

    class Meta:
        db_table = "Results"
