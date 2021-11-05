from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('lib_login/', views.lib_login, name = "lib_login"),
    path('stu_login/', views.stu_login, name = "stu_login"),
    path('librarian/', views.lib, name = "lib"),
    path('student/', views.stu, name="stu"),
    path('student/register/', views.register, name="register"),
    path('student/<str:stu>/', views.stu_home, name="stu_home"),
    path('librarian/<str:lib>/', views.lib_home, name="lib_home"),
    path('librarian/<str:lib>/add/', views.add, name="add"),
    path('librarian/<str:lib>/requestList', views.requestList, name="requestList"),
    path('librarain/<str:lib>/requestList/<int:stuId>', views.add2, name="add2"), 
    path('student/<str:stu>/search', views.stu_search, name="stu_search"),
    path('student/<str:stu>/book', views.book, name="book")
]