from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('mark-done/', views.mark_cleaning_done, name='mark_cleaning_done'),
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    path('warden/', views.warden_dashboard, name='warden_dashboard'),
]