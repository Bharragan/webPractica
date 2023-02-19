from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('flotacion/', views.flot, name="flotacion"),
    path("export_excel",views.downloadFlotation),
    path('flotation_prediction/',views.flotation_prediction),
    path('lixiviacion/<str:pk>/', views.lix, name="lixiviacion"),
]
