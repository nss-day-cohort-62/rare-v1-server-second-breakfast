from django.db.models import Count, Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Category

class CategoryView(ViewSet):
    """Rare Publishers category view"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single category"""
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all categories"""
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        
        Returns:
            Response -- JSON serialized category instance
        """
        serializer = CreateCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle PUT requests for a category
        
        Returns:
            Response -- Empty body with 204 status code
        """

        category = Category.objects.get(pk=pk)
        category.label = request.data["label"]
        category.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for a category"""
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories"""
    class Meta:
        model = Category
        fields = ('id', 'label')

class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label')
