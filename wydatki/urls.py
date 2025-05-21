from django.urls import path
from . import  views

urlpatterns = [
    path('', views.lista_wydatkow, name='lista_wydatkow'),
    path('wydatek/<int:pk>/', views.wydatek_szczegoly, name='wydatek_szczegoly'),


    path('upload/', views.Image.as_view(),      name='upload_image'),
    path('display/<int:pk>/', views.ImageDisplay.as_view(), name='image_display'),


    path('wydatek/nowy/', views.wydatek_nowy, name='wydatek_nowy'),

    path('wydatek/<int:pk>/edycja/', views.wydatek_edycja, name='wydatek_edycja'),
]

