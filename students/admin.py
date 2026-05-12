from django.contrib import admin
from .models import Student # Adicionado para o model Student criado em students/models.py 

admin.site.register(Student) # Reguistrar Student no admin do Django
