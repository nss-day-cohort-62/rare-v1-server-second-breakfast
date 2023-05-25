from datetime import datetime
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

        rare_user = RareUser.objects.annotate(
            subscribed = Count(
                "subscribers",
                filter=Q(subscribers__follower__user=request.auth.user, subscribers__ended_on=None)
            ),
            unsubscribed = Count(
            "subscribers",
            filter=Q(subscribers__follower__user=request.auth.user, subscribers__ended_on__isnull=False)
            )
        ).get(pk=pk)

        serializer = RareUserSerializer(rare_user)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all users
        Returns: JSON serialized list of users as Response"""
        rare_users = RareUser.objects.all()
        serializer = RareUserSerializer(rare_users, many=True)
        return Response(serializer.data)

    @action(methods=['post', 'put'], detail=True)
    def subscribe(self, request, pk):
        """Post and Put Requests so user can subscribe to other users"""
        author = RareUser.objects.get(pk=pk)
        subscriber = RareUser.objects.get(pk=request.auth.user.id)
        if request.method == 'POST':
            Subscription.objects.create(author=author, follower=subscriber, ended_on = None)
            return Response({'message': 'Subscribed to author!'}, status=status.HTTP_201_CREATED)
        elif request.method =='PUT':
            update_subscription = Subscription.objects.get(author=author, follower=subscriber)
            update_subscription.ended_on = None
            update_subscription.save()
            return Response({'message': 'Resubscribed!'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def unsubscribe(self, request, pk):
        """Put request so user can unsubscribe from an author"""
        subscription = Subscription.objects.get(author=pk, follower=request.auth.user.id)
        subscription.ended_on = datetime.now()
        subscription.save()
        return Response({'message': 'Unsubscribed'}, status=status.HTTP_204_NO_CONTENT)

class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for users
    """
    class Meta:
        model = RareUser
        fields = ('id', 'bio', 'created_on', 'active','subscriptions', 'subscribers', 'subscribed', 'unsubscribed', 'profile_image_url', 'user')
        depth = 2
