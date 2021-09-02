from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()

# The app URL configuration defines /recipes as the prefix
# If we register it again here the URL endpoint will be /recipes/recipes
# which is why this is blank
router.register('', views.RecipeViewSet, basename='recipe')

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
