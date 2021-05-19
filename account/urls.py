from django.urls import path

from account import views

app_name = "account"

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/<int:user_id>/', views.user_dashboard, name='dashboard'),
    path('edit_profile/<int:user_id>/', views.profile_edit, name='profile_edit'),
    path('phone_login/', views.phone_login, name='phone_login'),
    path('verify/<str:phone>/<int:rand_num>', views.verify, name='verify'),
    path('follow/', views.follow, name='follow'),
    path('unfollow/', views.unfollow, name='unfollow'),

]
