from django.conf.urls import url
from django.urls import path, include
from .views import CustomTokenObtainPairView
from . import views

urlpatterns = [
    url('api-auth/', include('rest_framework.urls')),
    url('', include('djoser.urls')),
    url('', include('djoser.urls.authtoken')),
    path('auth/login', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
]
