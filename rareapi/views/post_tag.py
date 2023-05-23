from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import PostTag, Tag, Post

class PostTagView(ViewSet):
    """PostTags view"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single post_tag
        Returns: Response -- JSON serialized user
        """
        post_tag = PostTag.objects.get(pk=pk)
        serializer = PostTagSerializer(post_tag)
        return Response(serializer.data)
    
    def list(self, request):
        """Handle GET requests to get list of post_tags
        Returns: Response -- JSON serialized list of post_tags"""
        post_tags = []
        post_id = request.query_params.get('post')
        if post_id:
            post_tags = PostTag.objects.filter(post=post_id)
        else:
            post_tags = PostTag.objects.all()

        serializer = PostTagSerializer(post_tags, many=True)
        return Response(serializer.data)

    def create(self, request, pk=None):
        """Handle POST operations
        Returns: Response -- JSON serialized tag instance"""
        post_tag = PostTag()
        tag = Tag.objects.get(pk=pk)
        post = Post.objects.get(pk=pk)
        post_tag.tag = tag
        post_tag.post = post
        post_tag.save()

        serialized = PostTagSerializer(post_tag)

        return Response(serialized.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        """Handle PUT requests for a post_tag
        
        Returns:
            Response -- Empty body with 204 status code
        """

        post_tag = PostTag.objects.get(pk=pk)
        post_tag.tag = request.data["tag"]
        # post_tag.post = request.data["post"]
        post_tag.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        """Handle DELETE requests for a post_tag"""
        post_tag = PostTag.objects.get(pk=pk)
        post_tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PostTagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags"""
    class Meta:
        model = PostTag
        fields = ('id', 'tag', 'post')
        depth = 1
