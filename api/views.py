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

# O decorador @api_view garante que a função só aceite o método GET,
# além de permitir que a resposta seja formatada automaticamente para JSON ou Web Browsable API.
@api_view(['GET'])
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
