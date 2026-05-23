import django_filters
from .models import Employee

class EmployeeFilter(django_filters.FilterSet):
    """
    Classe de filtro customizada para o modelo Employee.
    Permite criar regras de busca mais complexas do que o padrão.
    """

    # --- EXPLICAÇÃO DO PARÂMETRO ATUAL ---
    # field_name: Indica o nome exato do campo no banco de dados ('designation').
    # lookup_expr='iexact': Define a expressão de busca como "texto exato", mas ignora maiúsculas/minúsculas (Case-Insensitive).
    designation = django_filters.CharFilter(field_name='designation', lookup_expr='iexact')

    # --- OUTROS EXEMPLOS ÚTEIS QUE VOCÊ PODE ADICIONAR ---
    
    # 1. Filtro por aproximação/contém (Ex: /api/employees/?name=silva)
    # lookup_expr='icontains': Busca qualquer parte do texto, ignorando maiúsculas/minúsculas.
    # name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    # 2. Filtro de número maior ou igual a (Ex: /api/employees/?min_salary=3000)
    # lookup_expr='gte': Significa "Greater Than or Equal" (Maior ou igual a).
    # min_salary = django_filters.NumberFilter(field_name='salary', lookup_expr='gte')

    # 3. Filtro de data exata ou posterior (Ex: /api/employees/?joined_after=2026-01-01)
    # lookup_expr='gte': Pode ser usado em datas para buscar registros a partir daquele dia.
    # joined_after = django_filters.DateFilter(field_name='hire_date', lookup_expr='gte')

    class Meta:
        model = Employee  # Vincula este filtro ao modelo Employee.
        
        # O 'fields' aqui define quais campos terão filtros automáticos (gerados pelo Django).
        # Como 'designation' já foi declarado manualmente acima com regras customizadas,
        # você pode listar outros campos aqui para busca simples por igualdade exata.
        # Exemplo: fields = ['designation', 'department', 'is_active']
        fields = ['designation']
