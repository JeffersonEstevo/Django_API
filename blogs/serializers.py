from rest_framework import serializers
from .models import Blog, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    # Define a relação "um-para-muitos" (um blog para vários comentários).
    # many=True: indica que 'comments' é uma lista de objetos, não apenas um.
    # read_only=True: os comentários serão apenas exibidos na saída (GET), 
    # sem permitir criação/edição direta através deste campo no BlogSerializer.
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Blog
        fields = '__all__'
        