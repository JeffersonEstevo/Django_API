from django.contrib import admin
# Importa os modelos Blog e Comment do arquivo models.py da mesma pasta (.)
# O Django precisa disso para saber quais tabelas você quer exibir no painel de administração
from .models import Blog, Comment 

admin.site.register(Blog)     # Registra o modelo Blog para que ele apareça e possa ser editado no painel administrativo
admin.site.register(Comment)  # Registra o modelo Comment para gerenciar os comentários pelo painel administrativo
