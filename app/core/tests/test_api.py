import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Article, Tag, Category

from article.serializers import ArticleSerializer, ArticleDetailSerializer


ARTICLE_URL = reverse('article:article-list')


def image_upload_url(article_id):
    """Return URL for article image upload"""
    return reverse('article:article-upload-image', args=[article_id])


def detail_url(article_id):
    """Return article detail URL"""
    return reverse('article:article-detail', args=[article_id])


def sample_tag(user, name='Marvel', slug='mc'):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name, slug=slug)


def sample_category(user, name='Movie', slug='film'):
    """Create and return a sample ingredient"""
    return Category.objects.create(user=user, name=name, slug=slug)


def sample_article(user, **params):
    """Create and return a sample article"""
    defaults = {
        'title': 'Sample article',
        'content': 'text',
        'slug': 'sample-slug',
       # 'category_id': 3
    }
    defaults.update(params)

    return Article.objects.create(user=user, **defaults)


class PublicArticleApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(ARTICLE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateArticleApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@magal.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    # def test_retrieve_recipes(self):
    #     """Test retrieving a list of recipes"""
    #     sample_article(user=self.user)
    #     res = self.client.get(ARTICLE_URL)
    #
    #     articles = Article.objects.all().order_by('-id')
    #     serializer = ArticleSerializer(articles, many=True)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)

    # def test_view_article_detail(self):
    #     """Test viewing a recipe detail"""
    #     article = sample_article(user=self.user)
    #     article.tags.add(sample_tag(user=self.user))
    #     article.category.add(sample_category(user=self.user))
    #
    #     url = detail_url(article.id)
    #     res = self.client.get(url)
    #
    #     serializer = ArticleDetailSerializer(article)
    #     self.assertEqual(res.data, serializer.data)
