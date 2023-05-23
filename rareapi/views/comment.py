from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Comment, RareUser, Post

class CommentView(ViewSet):
    """Comment view"""

    def retrieve(self, request, pk=None):
        """Handle get requests for single comment"""
        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET request for all comments"""
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST request for comment"""

        author = RareUser.objects.get(user=request.auth.user)
        serializer = CreateCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle PUT request for update"""
        comment = Comment.objects.get(pk=pk)
        author = RareUser.objects.get(user=request.auth.user)
        comment.author = author
        post = Post.objects.get(pk=request.data['post'])
        comment.post = post
        comment.content = request.data['content']
        comment.created_on = request.data['created_on']
        comment.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE request"""
        comment=Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content','created_on')
        depth = 2

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'content', 'created_on')
