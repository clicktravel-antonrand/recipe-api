from rest_framework import viewsets

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def get_queryset(self):
        """Retrieve recipes with name filter"""
        name = self.request.query_params.get('name')
        queryset = Recipe.objects.all()
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset
