from rest_framework import serializers
from core.models import Tag, Category, Article

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
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Article
        fields = ('id', 'title', 'category', 'tags', 'author')
        read_only_fields = ('id',)

    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.user.email

    def get_category(self, obj):
        return obj.category.name


class ArticleDetailSerializer(ArticleSerializer):
    """Serialize a article detail"""
    Categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class ArticleImageSerializers(serializers.ModelSerializer):
    """serializer for uploading images to articles"""

    class Meta:
        model = Article
        fields = ('id', 'image')
        read_only_fields = ('id',)