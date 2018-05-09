from django.contrib.auth.models import User
from rest_framework import serializers, viewsets

from .models import Category, Post, Tag


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('url', 'id', 'title', 'desc', 'pv', 'created_time')


class PostDetailSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    owner = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Post
        fields = ('url', 'id', 'owner', 'title', 'desc', 'category', 'tags', 'pv', 'created_time')


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super(PostViewSet, self).retrieve(request, *args, **kwargs)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('url', 'id', 'name', 'is_nav', 'created_time')


class CategoryDetailSerializer(serializers.ModelSerializer):
    post_set = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('url', 'id', 'name', 'is_nav', 'created_time', 'post_set')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(status=1)
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super(CategoryViewSet, self).retrieve(request, *args, **kwargs)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('url', 'id', 'name', 'created_time')


class TagDetailSerializer(serializers.ModelSerializer):
    post_set = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ('id', 'name', 'created_time', 'post_set')


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.filter(status=1)
    serializer_class = TagSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = TagDetailSerializer
        return super(TagViewSet, self).retrieve(request, *args, **kwargs)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username')


class UserDetailSerializer(serializers.ModelSerializer):
    post_set = PostSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'post_set')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=True)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = UserDetailSerializer
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)
