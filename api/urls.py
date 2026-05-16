from django.urls import path
from . import views

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
    path('employees/', views.Employees.as_view()),
    
    # Mapeia a URL /employees/ (seguida da chave primária <int:pk> de um funcionário) 
    # para a classe 'EmployeeDetails'. O método .as_view() converte a classe 
    # em função para responder à requisição com os dados desse funcionário específico.
    path('employees/<int:pk>', views.EmployeeDetail.as_view()),
]
 

