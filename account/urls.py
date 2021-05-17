from django.urls import path

from account import views

app_name = "account"

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/<int:user_id>/', views.user_dashboard, name='dashboard')
]
