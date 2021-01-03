from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('all-courses/', views.allCourses, name="allCourses"),
    path('about/', views.about, name="about"),
    path('search/', views.search, name="search"),
    path('404/', views.notFound, name="notFound"),
    path('<slug:slug>/', views.post, name="post"),
]
