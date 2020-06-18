from django.conf.urls import url
from django.urls import path, include
from .views import CustomTokenObtainPairView
from . import views

urlpatterns = [
    url('api-auth/', include('rest_framework.urls')),
    url('', include('djoser.urls')),
    url('', include('djoser.urls.authtoken')),
    path('auth/us', views.restricted),
    path('auth/login', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    url('users/all', views.UserProfileListCreateView.as_view(), name="all-profiles"),
    url('dependants/', views.depend, name="dependants"),
    url('signup/', views.signup, name="signup"),
    url('user/auth', views.get_auth_user, name="auth-profile"),
    url('user/update', views.update_user, name="update-user"),
    url('dependant/update', views.update_dependant, name="update-dependant"),
    url('dependant/(?P<dep_id>\d+)', views.get_dependant, name="update-dependant"),
    # path(r'user/logout/', views.UserLogoutAllView.as_view(), name='user-logout-all'),
]

