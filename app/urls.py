from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('texts/', views.text_list, name='text_list'),
    path('texts/<int:pk>/', views.text_detail, name='text_detail'),
]
