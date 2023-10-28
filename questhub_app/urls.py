from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.loginpage, name='loginpage'),
    path('Register/',views.registerpage, name='registerpage'),
    path('User-Save',views.register_save,name='register_save'),
    path('User-login/',views.userlogin, name='userlogin'),
    path('logout/',views.userlogout, name='userlogout'),
    path('Home/',views.index, name='index'),
    path('Save-Question/',views.askquestion,name='askquestion'),
    path('Submit-answer/<int:pk>/',views.submit_answer,name='submit_answer'),
    path('View-answers/<int:pk>/',views.view_answers,name='view_answers'),
    path('Like-answer/<int:answer_id>/',views.like_answer,name='like_answer'),


]
