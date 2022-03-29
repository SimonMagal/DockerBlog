from django.urls import path, include
from rest_framework.routers import DefaultRouter

from article import views

router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('categories', views.CategoryViewSet)
router.register('articles', views.ArticleViewSet)

app_name = 'article'

urlpatterns = [
    path('', include(router.urls))
]