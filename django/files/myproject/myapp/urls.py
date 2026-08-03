from django.urls import path
from myapp import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('create/', views.create, name="create"),
    path('read/', views.read, name="read"),
    path("update/<int:id>/", views.update, name="update"),
    path("delete/<int:id>/", views.delete, name="delete"),
    path('course_create/', views.course_create, name="course_create"),
    path('signup/', views.signup, name="signup"),
]