from django.test import TestCase

from core import models


class ModelTests(TestCase):

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        recipe = models.Recipe.objects.create(
            name='Cheesy Chorizo Risotto',
            description='A simple to make risotto for 4',
        )

        ingredient = models.Ingredient.objects.create(
            recipe=recipe,
            name='Brown Onion'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            name='Cheesy Chorizo Risotto',
            description='A simple to make risotto for 4',
        )
        self.assertEqual(str(recipe), recipe.name)
