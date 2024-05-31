from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='dashboard'),
    path('register_user',views.register_user,name='register_user'),
    path('login_user',views.login_user,name='login_user'),
    path('logout_user',views.logout_user,name='logout_user'),
    path('upload_file',views.upload_file,name='upload_file'),
    path('search/',views.search,name='search'),
    path('createplaylist/',views.create_playlist,name='create_playlist'),
]