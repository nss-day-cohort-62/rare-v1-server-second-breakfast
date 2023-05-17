from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.viewsets import ViewSet
from rareapi.models import RareUser
from django.contrib.auth.models import User
from rest_framework.decorators import action

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for RareUsers"""

    class Meta:
        model = RareUser
        fields = ('id', 'created_on', 'bio')

class RareUserView(ViewSet):
    @action(detail=True, methods=['get'])
    def get(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            rareuser = RareUser.objects.get(user_id=pk)

            user_data = UserSerializer(user).data
            rareuser_data = RareUserSerializer(rareuser).data

            response_data = {**user_data, **rareuser_data}

            return Response(response_data)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)