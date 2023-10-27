from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.loginpage, name='loginpage'),
    path('Register/',views.registerpage, name='registerpage'),
    path('User-Save',views.register_save,name='register_save'),
    path('Home/',views.index, name='index'),
    path('User-login/',views.userlogin, name='userlogin'),
    path('logout/',views.userlogout, name='userlogout'),
]
