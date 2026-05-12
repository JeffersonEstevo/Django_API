from rest_framework import serializers
from students.models import Student

class StudentsSerializer(serializers.ModelSerializer):
    # A class Meta define a configuração do Serializer: vincula qual Model será 
    # transformado em JSON e quais campos devem ser incluídos na resposta.
    class Meta:
        model = Student
        fields = "__all__" # incluir todos os campos do model Student

    