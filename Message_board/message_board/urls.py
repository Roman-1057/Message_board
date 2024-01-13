from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from message import views
from message.views import UserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', UserView.as_view()),
    path('register/', views.register, name='register'),
    path('advertisement_detail/<int:ad_id>/', views.advertisement_detail, name='advertisement_detail'),
    path('create_advertisement/', views.create_advertisement, name='create_advertisement'),
    path('edit_advertisement/<int:ad_id>/', views.edit_advertisement, name='edit_advertisement'),
    path('create_response/<int:ad_id>/', views.create_response, name='create_response'),
    path('private_page/', views.private_page, name='private_page'),
    path('send_newsletter/', views.send_newsletter, name='send_newsletter'),

    path('user/login',
         LoginView.as_view(template_name='login.html'),
         name='login'),
    path('user/logout',
         LogoutView.as_view(template_name='logout.html'),
         name='logout'),

]
