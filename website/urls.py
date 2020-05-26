from django.urls import path
from django.conf.urls import  include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    #introducimos el sistema de autentificación
    path('accounts/', include('django.contrib.auth.urls')),    
    path("register/",  views.register,  name="register"),
    path("accounts/profile/",  views.private_index,  name="private_index"),
    path("accounts/details/",  views.myaccount_details,  name="my_account"),
    path('i18n/', include('django.conf.urls.i18n')),
    
#    path("accounts/password_reset/", views.password_reset, name = "password_reset"),
    #path('accounts/password/reset/', views.password_reset, name = "password_reset"),
    #path('accounts/password/confirm/', views.password_confirm, name = "password_confirm"),




]
