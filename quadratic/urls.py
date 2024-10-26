from django.urls import path
from . import views

urlpatterns = [
    path('', views.input_form, name='input_form'),
    path('solve/', views.solve_quadratic, name='solve_quadratic'),
]
