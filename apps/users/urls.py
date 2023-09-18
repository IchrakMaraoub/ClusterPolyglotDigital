from django.urls import path
from . import views 
from .views import  LoginView,UserLogout,LoginAPI
from knox import views as knox_views


app_name = 'users'
urlpatterns = [
    path('profile/', views.profile, name='user_profile'),
    path('profile/upload-image/', views.upload_profile_image, name='upload_profile_image'),
    path('api-keys/create/', views.create_api_key, name='create_api_key'),
    path('api-keys/revoke/', views.revoke_api_key, name='revoke_api_key'),
    path('login',LoginView.as_view(),name='login'),
    path('logout',UserLogout.as_view(),name='logout'),
    path('login_csrf/', LoginAPI.as_view(), name='login_csrf'),
    path('logout_csrf/', knox_views.LogoutView.as_view(), name='logout_csrf'),
]