from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url('appointments/user/upcoming', views.upcoming_appointment, name='upcoming_appointments'),
    url('appointments/user/past', views.past_appointment, name='past_appointments'),
    url('appointments/user/all', views.get_appointment, name='appointments'),
]
