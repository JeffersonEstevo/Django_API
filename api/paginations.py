# Importa a classe base de paginação por número de página do Django REST Framework.
from rest_framework.pagination import PageNumberPagination
# Importa a classe Response para retornar a resposta HTTP estruturada em JSON.
from rest_framework.response import Response

# Cria uma classe de paginação customizada herdando as funções da PageNumberPagination.
class CustomPagination(PageNumberPagination):
    # Permite que o cliente mude o tamanho da página via URL (ex: ?page_size=5).
    page_size_query_param = 'page_size'
    # Altera o parâmetro de tamanho da página na URL para 'page-num'.
    page_query_param = 'page-num'
    # Define o limite máximo estrito de itens que uma página pode conter (apenas 1 item).
    max_page_size = 1

    # Sobrescreve o método que estrutura o formato final do JSON retornado pela API.
    def get_paginated_response(self, data):
        # Retorna uma resposta HTTP com um dicionário contendo os metadados e os dados.
        return Response({
            # Gera o link URL para a próxima página de resultados (se houver).
            'next': self.get_next_link(),
            # Gera o link URL para a página anterior de resultados (se houver).
            'previous': self.get_previous_link(),
            # Exibe a quantidade total de registros existentes no banco de dados.
            'count': self.page.paginator.count,
            # Mostra explicitamente no JSON quantos itens estão sendo exibidos nesta página.
            'page_size': self.page_size,
            # Entrega a lista real de objetos/dados solicitados pelo cliente.
            'results': data
        })
