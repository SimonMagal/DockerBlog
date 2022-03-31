from rest_framework import serializers
from core.models import Tag, Category, Article, User


class TagSerializer(serializers.ModelSerializer):
    """serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    """serializer for Category objects"""

    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ArticleSerializer(serializers.ModelSerializer):
    """serialize a article"""
    category = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Category.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'category', 'tags', 'author', 'slug', 'image')
        read_only_fields = ('id',)

    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.user.email


class ArticleImageSerializers(serializers.ModelSerializer):
    """serializer for uploading images to articles"""

    class Meta:
        model = Article
        fields = ('id', 'image')
        read_only_fields = ('id',)


class ArticleDetailSerializer(ArticleSerializer):
    """Serialize a article detail"""
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    image = ArticleImageSerializers(read_only=True)
    lookup_field = 'slug'
    extra_kwargs = {
        'url': {'lookup_field': 'slug'}
    }


class UserSerializer(serializers.ModelSerializer):
    """serialize a user data to a list"""

    class Meta:
        model = User
        fields = ('id', 'name', 'email')
        read_only_fields = ('id',)
