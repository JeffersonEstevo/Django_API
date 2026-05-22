# Maneira provisória de listar Students 
    # from django.shortcuts import render
    # from django.http import JsonResponse
    # from students.models import Student 

    # def studentsView(request):
    #     # Busca todos os registros da tabela Student no banco de dados (retorna um QuerySet)
    #     students = Student.objects.all()   
        
    #     # Exibe os objetos no terminal/console para fins de depuração (debug)
    #     print(students) 

    #     # Converte o QuerySet (objetos do Django) em um formato de dicionário Python (lista de valores).
    #     # Isso é necessário porque o JsonResponse não consegue converter objetos complexos diretamente.
    #     students_list = list(students.values())

    #     # Retorna a lista no formato JSON. 
    #     # O 'safe=False' é obrigatório aqui porque, por padrão, o JsonResponse espera um 
    #     # dicionário (dict). Como estamos enviando uma lista (list), precisamos desativar essa trava.
    #     return JsonResponse(students_list, safe=False)

from django.shortcuts import render, get_object_or_404 # get_object_or_404 adicionado para Viewset
from students.models import Student
from .serializers import StudentsSerializer, EmployeeSerializer
from rest_framework.response import Response # Importa o Response do DRF, que é mais inteligente que o JsonResponse comum
from rest_framework import status # Importa códigos de status HTTP (200, 404, 201) para seguir o padrão REST
from rest_framework.decorators import api_view # Decorador que transforma a função em uma API de fato (adiciona interface e restrição de métodos)
from django.http import Http404 # Importa a exceção 404 nativa do Django (quando o usuário acessa um endereço que não existe, por exemplo).
# Importa os mixins e generics do Django Rest Framework (DRF)
# 'mixins' fornece os métodos de ação (list, create, retrieve, update, destroy)
# 'generics' fornece classes base e views prontas para reduzir a repetição de código (DRY)
from rest_framework import mixins, generics, viewsets


# Class-Based Views
# rest_framework.views: Módulo do DRF que gerencia o ciclo de vida das requisições HTTP da API.
# APIView: Classe base que gerencia autenticação, permissões e roteamento dos métodos HTTP (GET, POST, etc.).
from rest_framework.views import APIView 

# employees.models: Módulo da aplicação 'employees' onde as tabelas do banco de dados são estruturadas.
# Employee: Classe (Model) que permite criar, buscar, atualizar e deletar os registros de funcionários no banco.
from employees.models import Employee

from blogs.models import Blog, Comment # Adicionado para classes Blog e comment
from blogs.serializers import BlogSerializer, CommentSerializer # Adicionado para classes Blog e comment

# O decorador @api_view garante que a função só aceite os métodos GET e POST,
# além de permitir que a resposta seja formatada automaticamente para JSON ou Web Browsable API.
@api_view(['GET', 'POST'])
def studentsView(request):
    if request.method == 'GET':
        # Recupera todos os objetos do banco de dados (QuerySet)
        students = Student.objects.all()
        
        # O Serializer faz a ponte: ele pega os objetos complexos do Django e os "traduz" 
        # para tipos nativos do Python que podem virar JSON.
        # O 'many=True' avisa que estamos serializando uma lista (vários alunos), não apenas um.
        serializer = StudentsSerializer(students, many=True)
        
        # Seguindo o padrão REST, retornamos os dados serializados (serializer.data)
        # acompanhados do status HTTP 200 OK, confirmando que a requisição teve sucesso.
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # Pega os dados brutos enviados no corpo da requisição e joga no Serializer
        serializer = StudentsSerializer(data=request.data)
        
        # Valida se os dados respeitam as regras do modelo (campos obrigatórios, tipos, etc.)
        if serializer.is_valid():
            # Se estiver tudo ok, salva no banco de dados
            serializer.save()
            # Retorna o objeto criado com o status 201 (Created)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Se a validação falhar, imprime o erro no console para debug
        print(serializer.errors)
        # Retorna o que deu errado com o status 400 (Bad Request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Decorador que define que esta view só aceita requisições do tipo GET.
# Se receber POST, retorna automaticamente 405 Method Not Allowed.
@api_view(['GET', 'PUT', 'DELETE'])
def studentDetailView(request, pk):
    try:
        # Tenta buscar o estudante no banco de dados usando a chave primária (pk) recebida na URL.
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        # Se o estudante não existir, captura o erro e retorna uma resposta 404 (Not Found)
        # sem quebrar a aplicação.
        return Response(status=status.HTTP_404_NOT_FOUND)

    # 4. Verifica se o método é GET (o decorador acima já garante isso, 
    # mas esta verificação é boa prática caso a lista de métodos no @api_view aumente).
    if request.method == 'GET':
        # Instancia o Serializer passando o objeto 'student' encontrado, 
        # convertendo o model complexo em um formato JSON nativo (serialização).
        serializer = StudentsSerializer(student)
        
        # Retorna os dados serializados (JSON) com status 200 (OK).
        return Response(serializer.data, status=status.HTTP_200_OK)
    # Verifica se o método da requisição é PUT (atualização completa)
    elif request.method == 'PUT':
        # Inicializa o serializer com a instância existente (student) e os novos dados (request.data).
        # O student garante que estamos atualizando e não criando um novo.
        serializer = StudentsSerializer(student, data=request.data)
        
        # Valida se os dados enviados estão de acordo com as regras do serializer.
        if serializer.is_valid():
            # Salva as alterações no banco de dados se os dados forem válidos.
            serializer.save()
            
            # Retorna os dados atualizados com status 200 OK.
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Se inválido, retorna os erros de validação com status 400 Bad Request.
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    # Verifica se o método HTTP da requisição é 'DELETE'
    elif request.method == 'DELETE':
        # Chama o método .delete() no objeto 'student' (instância do modelo)
        # para remover o registro correspondente do banco de dados.
        student.delete()
        
        # Retorna uma resposta HTTP 204 (No Content), que é o padrão
        # para deleções bem-sucedidas, indicando que a requisição foi
        # processada, mas não há conteúdo para enviar de volta no corpo.
        return Response(status=status.HTTP_204_NO_CONTENT)

# # Define a classe 'Employees' herdando de 'APIView' para torná-la uma Class-Based View do Django REST Framework.
# class Employees(APIView):
    
#     # Define o método que intercepta e trata requisições HTTP do tipo GET.
#     def get(self, request):
        
#         # Busca todos os registros de funcionários cadastrados na tabela do banco de dados utilizando o ORM do Django.
#         employees = Employee.objects.all()
        
#         # Converte a lista de objetos do banco de dados (QuerySet) em dados nativos do Python (como dicionários).
#         # O argumento 'many=True' avisa ao serializer que ele irá processar múltiplos registros (uma lista), e não apenas um.
#         serializer = EmployeeSerializer(employees, many=True)
        
#         # Retorna uma resposta HTTP contendo os dados formatados em JSON e o código de status HTTP 200 (OK).
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         # Cria o serializer com os dados brutos enviados no corpo da requisição (JSON)
#         serializer = EmployeeSerializer(data=request.data)
        
#         # Verifica se os dados enviados respeitam as regras de validação do modelo/serializer
#         if serializer.is_valid():
#             # Se for válido, salva o objeto no banco de dados
#             serializer.save()
#             # Retorna os dados salvos e o status HTTP 201 (Created)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
#         # Se os dados forem inválidos, retorna os erros de validação e o status HTTP 400 (Bad Request)
#         # Nota: Geralmente usa-se serializer.errors aqui para mostrar o que deu errado
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

# class EmployeeDetail(APIView):
#     # Cria uma classe de visualização (View) baseada no Django REST Framework para lidar com solicitações de um funcionário específico.
    
#     def get_object(self, pk):
#         # Define um método auxiliar para buscar um funcionário específico usando sua Primary Key (pk / ID).
        
#         try:
#             # Inicia o bloco onde tentaremos executar a lógica de banco de dados.

#             return Employee.objects.get(pk=pk)
#             # Faz uma consulta no banco de dados para buscar o funcionário cujo ID (pk) corresponde ao passado na URL.
            
#         except Employee.DoesNotExist:
#             # Captura a exceção específica do Django caso o funcionário com esse 'pk' não exista no banco de dados.
            
#             raise Http404
#             # Interrompe a execução e retorna um erro 404 Not Found para o cliente, indicando que o recurso não foi localizado.
    
#     def get(self, request, pk):
#         # Define o método HTTP GET. Nota: adicionamos 'request' como primeiro argumento, pois ele recebe os dados da requisição HTTP.
        
#         employee = self.get_object(pk)
#         # Chama o método auxiliar acima para buscar o funcionário específico no banco de dados usando o 'pk'.
        
#         serializer = EmployeeSerializer(employee)
#         # Instancia o serializador, passando o objeto do funcionário para convertê-lo em um formato compatível com JSON.
        
#         return Response(serializer.data, status=status.HTTP_200_OK)
#         # Retorna a resposta HTTP com os dados serializados do funcionário e um status 200 OK (sucesso).

#     def put(self, request, pk): 
#         # Busca o funcionário no banco de dados usando a chave primária (pk) recebida na URL
#         employee = self.get_object(pk) 
        
#         # Prepara o serializer com os dados atuais do employee e os novos dados enviados na requisição (request.data)
#         serializer = EmployeeSerializer(employee, data=request.data) 
        
#         # Verifica se os dados enviados respeitam as regras de validação do serializer
#         if serializer.is_valid(): 
#             # Se válidos, salva as alterações (atualiza o registro no banco de dados)
#             serializer.save() 
            
#             # Retorna os dados atualizados em formato JSON com o status HTTP 200 (OK)
#             return Response(serializer.data, status=status.HTTP_200_OK) 
        
#         # Se os dados forem inválidos, retorna os erros de validação com o status HTTP 400 (Bad Request)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

#     def delete(self, request, pk): 
#         # Busca o funcionário no banco de dados usando a chave primária (pk)
#         employee = self.get_object(pk) # Nota: assumido o 'pk' aqui para consistência com o PUT
        
#         # Remove o registro do banco de dados
#         employee.delete() 
        
#         # Retorna uma resposta vazia informando que a exclusão foi bem-sucedida com status HTTP 204 (No Content)
#         return Response(status=status.HTTP_204_NO_CONTENT)

"""
# Definição da Class Employyes utilizando Mixings
class Employees(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    # Define a fonte de dados (queryset) que será utilizada para as operações
    queryset = Employee.objects.all()
    
    # Define o serializer responsável pela validação e serialização dos dados
    serializer_class = EmployeeSerializer

    # Manipula requisições HTTP GET para listar todos os funcionários
    def get(self, request):
        # Utiliza o método 'list' provido pelo mixin ListModelMixin
        return self.list(request) 

    # Manipula requisições HTTP POST para criar um novo funcionário
    def post(self, request):
        # Utiliza o método 'create' provido pelo mixin CreateModelMixin
        return self.create(request)
    
# Esta classe define uma view baseada em classe (CBV) para gerenciar um funcionário específico.
# Ela herda mixins que fornecem as ações padrão de ler, atualizar e deletar um registro.
# Operações que necessitam de uma chave primária
class EmployeeDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    
    # Define a fonte de dados (banco de dados) que a view irá consultar.
    queryset = Employee.objects.all()
    
    # Define a classe responsável por converter o modelo Employee em JSON e vice-versa.
    serializer_class = EmployeeSerializer

    # Trata requisições HTTP GET para buscar (exibir) os detalhes de um funcionário específico usando a chave primária (pk).
    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    # Trata requisições HTTP PUT para atualizar todos os dados de um funcionário específico.
    def put(self, request, pk):
        return self.update(request, pk)

    # Trata requisições HTTP DELETE para remover um funcionário específico do banco de dados.
    def delete(self, request, pk):
        return self.destroy(request, pk)
"""   

"""
# Generics Views
# Views Genéricas simplificam e reduzem o código repetitivo em APIs REST.

# Classe para lidar com a listagem e criação de funcionários (Collection Endpoint)
class Employees(generics.ListCreateAPIView):
    # Define o conjunto de dados base (busca todos os funcionários no banco)
    queryset = Employee.objects.all()
    
    # Define a classe que vai converter os dados do banco para JSON e vice-versa
    serializer_class = EmployeeSerializer

# Classe para lidar com operações focadas em um único funcionário (Instance Endpoint)
class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    # Define o conjunto de dados base onde a busca do elemento específico será feita
    queryset = Employee.objects.all()
    
    # Define a classe que vai converter os dados do registro específico para JSON
    serializer_class = EmployeeSerializer
    
    # Informa ao DRF qual campo do banco de dados usar para localizar o funcionário na URL
    # 'pk' significa Primary Key (o ID numérico padrão do Django). Exemplo: /employees/1/
    lookup_field = 'pk'
"""

"""
# Viewsets
# Define uma ViewSet básica que herda diretamente da classe genérica 'ViewSet'.
# Diferente de uma 'ModelViewSet', esta exige que você escreva a lógica de cada ação manualmente.
class EmployeeViewset(viewsets.ViewSet):
    
    # Método responsável por responder a requisições HTTP GET na raiz do endpoint (ex: /employees/).
    # Ele substitui a lógica que normalmente ficaria em uma função de listagem ou no método get().
    def list(self, request):
        
        # Busca todos os registros da tabela Employee no banco de dados.
        queryset = Employee.objects.all()
        
        # Instancia o serializador passando a lista de funcionários.
        # O argumento 'many=True' avisa ao Django que ele está processando uma lista (múltiplos objetos) e não apenas um registro.
        serializer = EmployeeSerializer(queryset, many=True)
        
        # Retorna uma resposta HTTP 200 OK contendo os dados já convertidos para o formato JSON (dentro de serializer.data).
        return Response(serializer.data)
    
    # Método responsável por responder a requisições HTTP POST no endpoint (ex: /employees/).
    # Ele lida com o recebimento de novos dados e a criação do registro no banco.
    def create(self, request):
        
        # Instancia o serializador passando os dados enviados pelo cliente no corpo da requisição (request.data).
        serializer = EmployeeSerializer(data=request.data)
        
        # Valida os dados recebidos com base nas regras definidas no EmployeeSerializer (ex: campos obrigatórios, tipos de dados).
        if serializer.is_valid():
            
            # Salva o novo registro de funcionário diretamente no banco de dados.
            serializer.save()
            
            # Retorna os dados do funcionário recém-criado em formato JSON com o status HTTP 201 (Created).
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Se a validação falhar, retorna os erros gerados (ex: "campo obrigatório ausente") com o status padrão 400 (Bad Request).
        return Response(serializer.errors)
    
     # Método responsável por responder a requisições HTTP GET para um registro específico (ex: /employees/1/).
    def retrieve(self, request, pk=None):
        # Busca o funcionário pelo ID (pk). Se não encontrar, interrompe o código e retorna um erro 404 (Não Encontrado) automaticamente.
        employee = get_object_or_404(Employee, pk=pk)
        
        # Instancia o serializador passando apenas o objeto do funcionário encontrado para convertê-lo em JSON.
        serializer = EmployeeSerializer(employee)
        
        # Retorna os dados convertidos com o status HTTP 200 OK confirmando o sucesso da busca.
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Método responsável por responder a requisições HTTP PUT para atualizar um registro específico (ex: /employees/1/).
    def update(self, request, pk=None):
        # Busca o funcionário existente no banco de dados; retorna 404 se ele não existir.
        employee = get_object_or_404(Employee, pk=pk)
        
        # Passa o objeto do banco E os novos dados recebidos do cliente (request.data) para que o serializador faça a substituição.
        serializer = EmployeeSerializer(employee, data=request.data)
        
        # Valida se os novos dados enviados atendem a todos os requisitos e regras do modelo.
        if serializer.is_valid():
            # Atualiza e salva as novas informações deste funcionário diretamente no banco de dados.
            serializer.save()
            # Retorna o registro do funcionário com as informações já atualizadas.
            return Response(serializer.data)
        
        # Se os dados enviados forem inválidos, retorna a lista de erros de validação.
        return Response(serializer.errors)
    
    # Método responsável por responder a requisições HTTP DELETE para remover um registro específico (ex: /employees/1/).
    def delete(self, request, pk=None):
        # Busca o funcionário pelo ID correspondente antes de prosseguir; impede o erro se o registro não existir.
        employee = get_object_or_404(Employee, pk=pk)
        
        # Executa a exclusão definitiva do registro do funcionário na tabela do banco de dados.
        employee.delete()
        
        # Retorna uma resposta sem corpo de texto com o status HTTP 204 No Content, que sinaliza sucesso na remoção.
        return Response(status=status.HTTP_204_NO_CONTENT)
    
"""

# Podemos encurtar as Viewsets acima com o seguinte Model Viewset
# Ao herdar de 'ModelViewSet', a classe ganha automaticamente TODAS as lógicas de CRUDL de fábrica.
# Ela elimina a necessidade de escrever os métodos list(), create(), retrieve(), update() e destroy() manualmente.
class EmployeeViewset(viewsets.ModelViewSet):
    
    # Define a fonte de dados padrão. O ModelViewSet usa essa linha para saber em qual tabela buscar os dados,
    # fazendo as consultas do banco de dados (QuerySets) automaticamente para cada um dos métodos internos.
    queryset = Employee.objects.all()
    
    # Define o serializador padrão. O ModelViewSet usa essa classe de forma automática para validar os dados
    # recebidos (no POST/PUT) e transformar os objetos do banco em formato JSON (no GET).
    serializer_class = EmployeeSerializer

# generics.ListCreateAPIView ativa automaticamente os métodos HTTP GET (lista) e POST (criação).
class BlogsView(generics.ListCreateAPIView):
    # Define a base de dados (todos os registros) que a view irá consultar.
    queryset = Blog.objects.all()
    # Especifica o serializer que vai validar a entrada (POST) e estruturar a saída (GET).
    serializer_class = BlogSerializer

class CommentsView(generics.ListCreateAPIView):
    # Define a base de dados contendo todos os comentários cadastrados.
    queryset = Comment.objects.all()
    # Especifica o serializer responsável por processar os dados dos comentários.
    serializer_class = CommentSerializer

class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'
