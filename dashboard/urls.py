from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('devotee/', views.devotee_dashboard, name='devotee_dashboard'),
    path('leader/', views.leader_dashboard, name='leader_dashboard'),
    path('devotee/chat/', views.bhakti_ai_chat, name='bhakti_ai_chat'),
    path('devotee/seva/complete/<int:seva_id>/', views.complete_seva, name='complete_seva'),
    path('notifications/unread/', views.get_unread_notifications, name='unread_notifications'),
    path('notifications/read/', views.mark_notifications_read, name='mark_notifications_read'),
    path('devotee/out-of-station/', views.toggle_out_of_station, name='toggle_out_of_station'),
    path('leader/manage-service/', views.manage_service, name='manage_service'),
    path('leader/assign-service/', views.assign_service, name='assign_service'),
    path('leader/weekly-report/', views.generate_weekly_report, name='generate_weekly_report'),
]
