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

    # field_name='emp_name': Aponta para a coluna 'emp_name' na tabela Employee do banco de dados.
    # lookup_expr='icontains': Transforma a busca em um "CONTÉM" que ignora maiúsculas/minúsculas (Case-Insensitive).
    # Exemplo: Se buscar por 'jo', a API vai retornar 'João', 'Anajô' ou 'Jonathan'.
    emp_name = django_filters.CharFilter(field_name='emp_name', lookup_expr='icontains')

    # RangeFilter: Cria automaticamente dois campos de busca na API para trabalhar com intervalos (Mínimo e Máximo).
    # Na prática, gera os parâmetros de URL: '?id_min=valor' e '?id_max=valor'.
    # Exemplo: /api/employees/?id_min=10&id_max=20 (Retorna os funcionários com IDs de 10 a 20).
    #id = django_filters.RangeFilter(field_name='id')

    # method='filter_by_id_range': Indica que a filtragem não será automática; o Django chamará a função 
    # 'filter_by_id_range' para processar o valor.
    # label: Altera o texto de exibição que aparece na interface visual da API (Django Browseable API).
    id_min = django_filters.CharFilter(method='filter_by_id_range', label='From EMP ID')
    id_max = django_filters.CharFilter(method='filter_by_id_range', label='To EMP ID')

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
        # Adicionado emp_name para registrar formalmente o campo de busca por nome na estrutura do filtro.
        # Garante que o campo customizado 'emp_name' seja reconhecido e exibida na interface da API
        # Adicionado id para mapear o RangeFilter na estrutura do FilterSet.
        # Permite que a API reconheça as propriedades de intervalo para a chave primária (ID).
        #fields = ['designation', 'emp_name', 'id']
        
        # Registra os parâmetros customizados 'id_min' e 'id_max' na estrutura do FilterSet.
        # Necessário para que a API reconheça e exponha essas duas chaves na URL e nos formulários.
        fields = ['designation', 'emp_name', 'id_min', 'id_max']

    # Este método é executado automaticamente quando 'id_min' ou 'id_max' são passados na URL.
    # Parâmetros recebidos pelo Django:
    # - queryset: A lista atual de resultados do banco de dados antes deste filtro ser aplicado.
    # - name: O nome do filtro que chamou o método (receberá a string 'id_min' ou 'id_max').
    # - value: O valor digitado pelo usuário na URL (ex: o ID '10').
    def filter_by_id_range(self, queryset, name, value):
        # Se a URL contiver '?id_min=X', filtra funcionários com emp_id MAIOR OU IGUAL (gte) a X.
        if name == 'id_min':
            return queryset.filter(emp_id__gte=value)
        
        # Se a URL contiver '?id_max=Y', filtra funcionários com emp_id MENOR OU IGUAL (lte) a Y.
        elif name == 'id_max':
            return queryset.filter(emp_id__lte=value)
        
        # Se o nome do filtro não corresponder a nenhum, retorna a lista original sem alterações.
        return queryset
    