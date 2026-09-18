from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

app_name = 'core'
urlpatterns = [
    path('login/', obtain_auth_token, name='obtain_auth_token'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('create/', views.RegistrationView.as_view(), name="register"),
    path('update/', views.AccountInfoUpdate.as_view(),name='update')
]