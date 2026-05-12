# Arquivo criado após adição do app com comando 'python .\manage.py startapp students'
# Este arquivo não é criado por padrão pelo Django

from django.urls import path
from . import views

urlpatterns = [
    path('', views.students),
]