from django.urls import path

from posts import views

app_name = 'posts'
urlpatterns = [
    path('', views.all_posts, name='all_posts'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>', views.post_detail, name='post_detail')
]
