from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Tag

class TagView(ViewSet):
    """Tags view"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single tag
        Returns: Response -- JSON serialized user
        """
        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get list of tags
        Returns: Response -- JSON serialized list of tags"""
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns: Response -- JSON serialized tag instance"""
        new_tag = Tag()
        new_tag.label = request.data['label']
        new_tag.save()

        serialized = TagSerializer(new_tag)

        return Response(serialized.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        """Handle PUT requests for a tag
        
        Returns:
            Response -- Empty body with 204 status code
        """

        tag = Tag.objects.get(pk=pk)
        tag.label = request.data["label"]
        tag.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        """Handle DELETE requests for a tag"""
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags"""
    class Meta:
        model = Tag
        fields = ('id', 'label')
