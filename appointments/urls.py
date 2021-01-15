from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url('appointments/user/upcoming', views.upcoming_appointment, name='upcoming_appointments'),
    url('appointments/user/past', views.past_appointment, name='past_appointments'),
    url('appointments/user/all', views.get_appointment, name='appointments'),
    url('appointments/user/book', views.book_appointment, name='book_appointments'),
    url('appointments/user/reschedule/(?P<app_id>\d+)', views.reschedule_appointment, name='book_appointments'),
    url('appointments/user/accept/(?P<app_id>\d+)', views.accept_appointment, name='accept_appointments'),
    url('appointments/user/reject/(?P<app_id>\d+)', views.reject_appointment, name='reject_appointments'),

    url('user/treatment', views.get_treatment, name='treatments'),
]
