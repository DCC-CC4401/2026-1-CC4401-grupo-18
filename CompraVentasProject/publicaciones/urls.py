from django.urls import path 
from . import views

urlpatterns= [ 
    path('publicaciones/', views.publicaciones, name='publicaciones'),
    path('buscar/', views.buscar, name= 'buscar'),
    path('publicar/', views.publicar, name='publicar')
]