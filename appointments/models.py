from django.db import models
from authApp.models import *


class Appointments(models.Model):
    aid = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appntmnt_date = models.DateField()
    app_status = models.CharField(max_length=50)
    visit_type = models.CharField(max_length=50)
    app_type = models.CharField(max_length=50)
    owner = models.CharField(default="Personal", max_length=50)
    dependant = models.CharField(max_length=80, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Appointments"


class BookAppointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appntmnt_date = models.DateField()
    app_type = models.CharField(max_length=50, blank=True, null=True)
    approval_status = models.CharField(max_length=50, default="Pending")
    book_type = models.CharField(max_length=50, default="New")
    book_id = models.ForeignKey(Appointments, on_delete=models.CASCADE, blank=True, null=True)
    reason = models.CharField(max_length=50, blank=True, null=True)
    comments = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        db_table = "Booked_Appointments"
