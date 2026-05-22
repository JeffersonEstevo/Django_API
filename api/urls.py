from django.urls import path, include # include adicionado para Viewsets
from . import views
from rest_framework.routers import DefaultRouter # Adicionado para Viewsets

# Instancia o gerenciador de rotas padrão do Django REST Framework.
# Ele cria automaticamente URLs estruturadas para todas as ações do ViewSet (como listar, criar e deletar).
router = DefaultRouter() # Adicionado para Viewsets 

# Registra o ViewSet no roteador para gerar as URLs correspondentes.
# 'employees': Define o prefixo da URL no navegador (ex: /employees/ e /employees/1/).
# views.EmployeeViewset: A classe que contém a lógica de negócio do endpoint.
# basename='employee': O nome base usado pelo Django para identificar internamente os nomes dessas rotas.
router.register('employees', views.EmployeeViewset, basename='employee')

urlpatterns = [
    # Function-Based Views (Views Baseadas em Funções)
    # Sempre que o usuário acessar a URL base /students/ (ex: ://dominio.com), 
    # o Django chama a função studentsView localizada no arquivo 'views.py'.
    path('students/', views.studentsView), 
    
    # Sempre que o usuário acessar /students/ seguido de um número inteiro (ex: /students/5), 
    # o Django captura esse número (pk - Primary Key), armazena na variável 'pk' 
    # e envia para a função studentDetailView exibir os detalhes daquele estudante específico.
    path('students/<int:pk>', views.studentDetailView),

    # Class-Based Views (Views Baseadas em Classes)
    # Mapeia a URL /employees/ para a classe 'Employees'. O método .as_view() 
    # é obrigatório aqui: ele converte a classe em uma função padrão do Django 
    # capaz de lidar com as requisições web.
    #path('employees/', views.Employees.as_view()),
    
    # Mapeia a URL /employees/ (seguida da chave primária <int:pk> de um funcionário) 
    # para a classe 'EmployeeDetails'. O método .as_view() converte a classe 
    # em função para responder à requisição com os dados desse funcionário específico.
    # path('employees/<int:pk>', views.EmployeeDetail.as_view()),

    # Inclui todas as URLs geradas automaticamente pelo roteador no padrão de caminhos da aplicação.
    # O caminho '' vazio significa que as rotas do roteador começam diretamente na raiz deste arquivo de URLs.
    path('', include(router.urls)), # Rota do Viewset

    # Mapeia a URL '/blogs/' para a view que lista e cria blogs.
    # .as_view(): transforma a classe da APIView em uma função que o Django consegue executar.
    path('blogs/', views.BlogsView.as_view()),
    
    # Mapeia a URL '/comments/' para a view que lista e cria comentários de forma geral.
    path('comments/', views.CommentsView.as_view()),

]
 

