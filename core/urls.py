from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='obtain_auth_token'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', views.RegistrationView.as_view(), name="register_account"),
    path('accounts/update/', views.AccountUpdate.as_view(),name='update_account'),
    path('view-profile/', views.ProfileView.as_view(), name='profile_view')
]