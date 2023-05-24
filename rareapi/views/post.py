"""View module for handling requests about posts"""
from django.http import HttpResponseServerError
from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rareapi.models import Post, RareUser, Category, Tag, Reaction

class PostView(ViewSet):
    """Rare posts view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post
        """
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all posts

        Returns:
            Response -- JSON serialized list of posts
        """
        posts = []

        if request.auth.user:
            posts = Post.objects.all()

            author = request.query_params.get('author', None)
            if author is not None:
                posts = posts.filter(user_id=author)

            category = request.query_params.get('category', None)
            if category is not None:
                posts = posts.filter(category_id=category)

            # tag = request.query_params.get('tag', None)
            # if tag is not None:
            #     posts = posts.filter(tag_id=tag)

            tag = request.query_params.get('tag', None)
            if tag is not None:
                tag_array = [int(t) for t in tag.split(',')]
                for tag_id in tag_array:
                    posts = posts.filter(tag=tag_id)


            search = request.query_params.get('search', None)
            if search is not None:
                posts = posts.filter(
                    Q(title__icontains=search) |
                    Q(content__icontains=search)
                )

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized post instance
        """
        user = RareUser.objects.get(user=request.auth.user)
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        saved_post = serializer.save(user=user)
        saved_post.tag.set(request.data['tag'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handle PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """

        post = Post.objects.get(pk=pk)
        category = Category.objects.get(pk=request.data["category"])
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]
        post.category = category
        post.tag.set(request.data['tag'])

        post.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Delete request for a post"""
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @ action(methods=["get"], detail=False)
    def myposts(self, request):
        """Get method for my posts"""
        user = RareUser.objects.get(user=request.auth.user)
        posts = Post.objects.filter(user=user)

        try:
        # if posts.user == user:
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response({"message": "This post isn't yours, authenticated user."}, status=404)

class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts"""
    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved', 'reaction', 'tag')
        depth = 2

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved', 'reaction', 'tag')
