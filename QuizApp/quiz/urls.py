from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('exam/', views.take_exam, name='take_exam'),
    path('submit/', views.submit_exam, name='submit_exam'),
]