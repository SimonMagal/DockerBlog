from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Category, Article
from article import serializers



class BaseArticleAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Base viewset for user owned article attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """create a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseArticleAttrViewSet):
    """manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class CategoryViewSet(BaseArticleAttrViewSet):
    """manage Categorys in database"""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """manage articles in the database"""
    serializer_class = serializers.ArticleSerializer
    queryset = Article.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """retrieve the articles for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """return appropiate serializer class"""
        if self.action == 'retrieve':
            return serializers.ArticleDetailSerializer
        elif self.action == 'upload_image':
            return serializers.ArticleImageSerializers

        return self.serializer_class

    def perform_create(self, serializer):
        """create a new article"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """upload an image to a article"""
        article = self.get_object()
        serializer = self.get_serializer(
            article,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )