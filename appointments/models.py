from django.db import models
from authApp.models import *


class Appointments(models.Model):
    aid = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appntmnt_date = models.DateField()
    app_status = models.CharField(max_length=50)
    visit_type = models.CharField(max_length=50)
    app_type = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Appointments"
