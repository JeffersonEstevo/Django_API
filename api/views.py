from django.shortcuts import render
from django.http import JsonResponse
from students.models import Student # Para puxar dados dinamicamente

def studentsView(request):
    # students = {
    #     'id': 1,
    #     'name': 'Andre',
    #     'class': 'Computer Science'
    # }

    # Adicionar estudantes dinamicamente
    students = Student.objects.all()   
    print(students) 
    # Serializar para converter dados da consulta em uma lista (Não é padrão Rest)
    students_list = list(students.values())
    return JsonResponse(students_list, safe=False) # safe=False para que possamos mandar um query como retorno, e não um Json como esperado
