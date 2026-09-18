from django.urls import path
from . import views

app_name = 'farms'

urlpatterns = [
    path('add-farm/', views.FarmRegistrationView.as_view(), name='add_farm'),
    path('farms-list/', views.FarmListView.as_view(), name='farm_list'),
    path('farm-details/', views.FarmDetailView.as_view(), name='farm_details'),
    path('farm-activity/', views.FarmActivityView.as_view(), name='farm_activity')
]