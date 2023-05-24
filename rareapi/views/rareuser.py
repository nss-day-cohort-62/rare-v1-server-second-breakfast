import datetime
from django.http import HttpResponseServerError
from django.db.models import Q, Count
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from rareapi.models import RareUser, Subscription


class RareUserView(ViewSet):
    """Rare users view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single user
        Returns: JSON serialized user as Response"""
        try:
            subscription = Subscription.objects.get(follower_id=request.auth.user.id, author_id=pk)
            rareuser = RareUser.objects.annotate(
                subscribed = Count(
                    "subscribers",
                    filter=Q(subscribers=subscription)
                )
            ).get(pk=pk)
        except Subscription.DoesNotExist:
            rareuser = RareUser.objects.get(pk=pk)
            rareuser.subscribed = 0
        serializer = RareUserSerializer(rareuser)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all users
        Returns: JSON serialized list of users as Response"""
        rareusers = RareUser.objects.all()
        serializer = RareUserSerializer(rareusers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get(self, request, pk=None):
        """Get request on rare users"""
        try:
            user = User.objects.get(pk=pk)
            rareuser = RareUser.objects.get(user_id=pk)

            user_data = UserSerializer(user).data
            rareuser_data = RareUserSerializer(rareuser).data

            response_data = {**user_data, **rareuser_data}

            return Response(response_data)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post', 'put'], detail=True)
    def subscribe(self, request, pk):
        """Post and Put Requests so user can subscribe to other users"""
        author = RareUser.objects.get(pk=pk)
        subscriber = RareUser.objects.get(pk=request.auth.user.id)
        if request.method == 'POST':
            created_on = request.data[datetime.now()]
            Subscription.objects.create(author=author, follower= subscriber, created_on=created_on, ended_on = None)
            return Response({'message': 'Subscribed to author!'}, status=status.HTTP_201_CREATED)
        elif request.method =='PUT':
            update_subscription = Subscription.objects.get(author=author, subscriber=subscriber)
            update_subscription.created_on = datetime.now()
            update_subscription.ended_on = None
            update_subscription.save()
            return Response({'message': 'Resubscribed!'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def unsubscribe(self, request, pk):
        """Put request so user can unsubscribe from an author"""
        subscription = Subscription.objects.get(author=pk, follower=request.auth.user.id)
        subscription.ended_on.add(datetime.now())
        return Response({'message': 'Unsubscribed'}, status=status.HTTP_204_NO_CONTENT)

class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for users
    """
    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'created_on', 'active','subscriptions', 'subscribers')
        depth = 1

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        depth = 1
