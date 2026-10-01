from django.urls import path
from . import views

app_name = 'farms'

urlpatterns = [
    path('add-farm/', views.FarmRegistrationView.as_view(), name='add_farm'),
    path('farms-list/', views.FarmListView.as_view(), name='farm_list'),
    path('farm-details/<int:id>/', views.FarmDetailView.as_view(), name='farm_details'),
    path('farm-house-details/<int:id>/', views.HouseDetail.as_view(), name='house_details'),
    path('farm-house/register-device/', views.RegisterBot.as_view(), name='register_bot'),
    path('add-house/', views.RegisterHouse.as_view(), name='register_house')
]