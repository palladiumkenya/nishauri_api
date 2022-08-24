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
    url('signup/', views.signup, name="signup"),
    url('verify/', views.verify_otp, name="verify-otp"),
    url('user/auth', views.get_auth_user, name="auth-profile"),
    url('user/update', views.update_user, name="update-user"),
    url('migrate/', views.migrate_data, name="migrate db"),

    url('dependant/update', views.update_dependant, name="update-dependant"),
    url('dependant/single', views.get_dependant, name="get-dependant"),
    url('approve/dependant/(?P<dep_id>\d+)', views.approve_dep, name="approve-dependant"),
    url('dependants/', views.depend, name="dependants"),
    url('update-positive/(?P<dep_id>\d+)', views.elevate_dependant, name="add-positive-dependant"),

    url('auth/dashboard', views.dashboard, name="dashboard"),
    url('user/regiment', views.regiment_history, name="regiment-history"),

    url('facilities/all', views.get_facilities_all, name="all-facilities"),
    # Chat
    url('chat/initiate', views.chat_initiate, name="chat-initiate"),
    url('chatrooms', views.chat_rooms, name="chat-rooms"),
    url('chats/recent', views.chat_recent, name="chat-recent"),
    url('chat/message', views.chat_message, name="chat"),
    url('chats/room/all', views.chat_history, name="chat-history"),

    url('web/dash', views.web_dash, name="web-dash"),
    url('user/create', views.create_users, name="user-create-admin"),
    url('web/clients/reg', views.clients_list, name="clients-list"),
    url('web/partner/list', views.partners_list, name="partners-list"),
    url('web/partner/ushauri', views.partners_ushauri, name="partners-list"),
    # path(r'user/logout/', views.UserLogoutAllView.as_view(), name='user-logout-all'),
]
