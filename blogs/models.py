from django.db import models  # Importa as ferramentas de banco de dados do Django

class Blog(models.Model):  # Cria a tabela 'Blog' no banco de dados
    blog_title = models.CharField(max_length=100)  # Cria um campo de texto curto (título) limitado a 100 caracteres
    blog_body = models.TextField()  # Cria um campo de texto longo para o conteúdo do post
    
    def __str__(self):  # Define como o objeto aparece no painel de admin ou logs
        return self.blog_title  # Faz com que o post seja identificado pelo título

class Comment(models.Model):  # Cria a tabela 'Comment' (comentários)
    # Cria uma relação: cada comentário pertence a um Blog. Se o Blog for deletado, os comentários também são (CASCADE)
    # Define uma relação de chave estrangeira onde cada comentário pertence a um blog.
    # related_name='comments': Cria um "atalho" ou relação reversa no modelo Blog.
    # Isso permite acessar todos os comentários de um blog usando 'blog.comments.all()'.
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments') 
    
    comment = models.TextField()  # Cria um campo de texto longo para o comentário (faltou os parênteses no seu original)
    
    def __str__(self):  # Define a representação do comentário
        return self.comment  # Faz com que o comentário seja identificado pelo seu próprio texto
    