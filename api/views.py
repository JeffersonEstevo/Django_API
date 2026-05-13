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

from students.models import Student
from .serializers import StudentsSerializer
from rest_framework.response import Response # Importa o Response do DRF, que é mais inteligente que o JsonResponse comum
from rest_framework import status             # Importa códigos de status HTTP (200, 404, 201) para seguir o padrão REST
from rest_framework.decorators import api_view # Decorador que transforma a função em uma API de fato (adiciona interface e restrição de métodos)

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
@api_view(['GET', 'PUT'])
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
        