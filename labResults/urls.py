from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    url('lab/vload', views.get_vload, name='vload'),
]
