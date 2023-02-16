from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('flotacion/', views.flot, name="flotacion"),
    path('lixiviacion/<str:pk>/', views.lix, name="lixiviacion"),
]
