

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


# RECIPES_URL = reverse('article:articles')


def image_upload_url(article_id):
    """Return URL for article image upload"""
    return reverse('article:article-upload-image', args=[article_id])


def detail_url(article_id):
    """Return article detail URL"""
    return reverse('article:article-detail', args=[article_id])


def sample_tag(user, name='Main course', slug='mc'):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name, slug=slug)


def sample_ingredient(user, name='Cinnamon', slug='cin'):
    """Create and return a sample ingredient"""
    return Category.objects.create(user=user, name=name, slug=slug)


def sample_article(user, **params):
    """Create and return a sample article"""
    defaults = {
        'title': 'Sample article',
        'content': 'text',
        'slug': 'sample-slug'
    }
    defaults.update(params)

    return Article.objects.create(user=user, **defaults)
