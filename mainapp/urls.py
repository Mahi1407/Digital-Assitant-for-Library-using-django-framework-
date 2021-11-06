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
    path('librarian/<str:lib>/add_book/', views.add_bookcopy, name="add_bookcopy"),
    path('librarian/<str:lib>/add_author/', views.add_author, name ="add_author"),
    path('librarian/<str:lib>/add_newbook/', views.add_newbook, name="add_newbook"),
    path('student/<str:stu>/search', views.stu_search, name="stu_search"),
    path('student/<str:stu>/book', views.book, name="book"),
    path('student/<str:stu>/book/<int:b>', views.book2, name="book2"),
    path('student/<str:stu>/BookList', views.stu_books, name = "stu_books"),
    path('student/<str:stu>/TotalFine', views.stu_fine, name="stu_fine"),
    path('student/<str:stu>/extension', views.extension, name="extension"),
    path('student/<str:stu>/extend/<int:bId>', views.extend, name="extend"),
    
]