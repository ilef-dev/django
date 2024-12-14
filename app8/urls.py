from django.urls import path
from . import views

urlpatterns = [
    path('solve/', views.generate_equation, name='generate_equation'),
    path('solve/check/', views.check_solution, name='check_solution'),
]