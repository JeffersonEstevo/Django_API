from django.db import models


# Esta classe representa uma tabela no banco de dados. 
# Cada atributo (student_id, name, branch) será uma coluna na tabela.
class Student(models.Model):
    student_id = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)

    # O método __str__ define como o objeto será exibido em texto (ex: no Django Admin)
    def __str__(self):
        return self.name
