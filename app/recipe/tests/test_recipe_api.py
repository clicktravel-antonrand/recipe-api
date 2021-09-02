from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient

from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def recipe_url(recipe_id):
    """Return URL for a recipe"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_recipe(params={}):
    """Create and return a sample recipe"""
    defaults = {
        'name': 'Cashew curry',
        'description': 'Low carb lunch packed with iron rich '
                       'veggies, crunchy cashews and chicken',
    }
    defaults.update(params)
    return Recipe.objects.create(**defaults)


def sample_ingredient(recipe, name='Cheese'):
    """Create and return a sample ingredient"""
    return Ingredient.objects.create(recipe=recipe, name=name)


class RecipeApiTests(TestCase):
    """Test Recipe API endpoints"""

    def setUp(self):
        self.client = APIClient()

    # GET /recipes/
    def test_get_all_recipes(self):
        """Test retrieving a list of recipes"""
        # Given
        sample_recipe()
        recipe = sample_recipe({
            'name': 'Turkey bubble & squeak',
            'description': 'An easy, lean, recipe'
        })
        recipe.ingredients.add(sample_ingredient(recipe=recipe, name='Turkey'))

        all_recipes = Recipe.objects.all().order_by('id')
        serializer = RecipeSerializer(all_recipes, many=True)

        # When
        res = self.client.get(RECIPES_URL)

        # Then
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    # GET /recipes/?name=<filter_term>
    def test_get_all_recipes_with_name_filter(self):
        """Test retrieving a list of filtered recipes"""
        # Given
        sample_recipe()
        recipe = sample_recipe({
            'name': 'Turkey bubble & squeak',
            'description': 'An easy, lean, recipe'
        })

        serializer = RecipeSerializer(recipe)

        # When
        filter_term = 'bubble'
        res = self.client.get(
            RECIPES_URL,
            {'name': filter_term}
        )

        # Then
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer.data, res.data)

    def test_get_all_recipes_with_name_filter_case_insensitive(self):
        """Test retrieving a list of filtered recipes is case insensitive"""
        # Given
        sample_recipe()
        recipe = sample_recipe({
            'name': 'Turkey bubble & squeak',
            'description': 'An easy, lean, recipe'
        })

        serializer = RecipeSerializer(recipe)

        # When
        filter_term = 'turkey'
        res = self.client.get(
            RECIPES_URL,
            {'name': filter_term}
        )

        # Then
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer.data, res.data)

    def test_get_all_recipes_with_name_filter_no_results(self):
        """Test retrieving a list of recipes when
        there are no filter matches"""
        # Given
        sample_recipe({
            'name': 'Turkey bubble & squeak',
            'description': 'An easy, lean, recipe'
        })

        # When
        filter_term = 'Pizza'
        res = self.client.get(
            RECIPES_URL,
            {'name': filter_term}
        )

        # Then
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)

    # GET /recipes/<id>/
    def test_get_recipe_by_id_success(self):
        """Test retrieving a recipe by ID"""
        # Given
        sample_recipe()
        recipe = sample_recipe({
            'name': 'Turkey bubble & squeak',
            'description': 'An easy, lean, recipe'
        })
        recipe.ingredients.add(sample_ingredient(recipe=recipe, name='Turkey'))

        serializer = RecipeSerializer(recipe)

        # When
        url = recipe_url(recipe.id)
        res = self.client.get(url)

        # Then
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_by_id_not_found(self):
        """Test retrieving a recipe by ID when the recipe doesn't exist"""
        # Given
        # No recipes defined

        # When
        res = self.client.get(recipe_url(recipe_id=1))

        # Then
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    # POST /recipes/
    def test_create_recipe(self):
        """Test creating a new recipe"""
        # Given
        payload = {
            'name': 'Pizza',
            'description': 'Put it in the oven',
            'ingredients': [
                {'name': 'cheese'},
                {'name': 'dough'},
                {'name': 'tomato'},
            ]
        }

        # When
        res = self.client.post(RECIPES_URL, payload)

        # Then
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()

        self.assertEqual(ingredients.count(), 3)

    def test_create_recipe_invalid_request(self):
        """Test creating a new recipe with invalid payload"""
        # Given
        payload = {
            'name': '',
        }

        # When
        res = self.client.post(RECIPES_URL, payload)

        # Then
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # PATCH /recipes/<id>/
    def test_patch_recipe(self):
        """Test partial update of a recipe"""
        # Given
        recipe = sample_recipe()

        ingredient1 = sample_ingredient(recipe, name='Sweetcorn')
        ingredient2 = sample_ingredient(recipe, name='Ham')

        recipe.ingredients.add(ingredient1, ingredient2)

        # When
        new_ingredient_name = 'Pepperoni'
        payload = {
            'name': recipe.name,
            'description': recipe.description,
            'ingredients': [
                {'name': new_ingredient_name}
            ]
        }

        res = self.client.patch(recipe_url(recipe_id=recipe.id), payload)

        # Then
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 1)
        self.assertEqual(new_ingredient_name, ingredients[0].name)

    # DELETE /recipes/<id>/
    def test_delete_recipe(self):
        """Test deleting an existing recipe"""
        # Given
        recipe = sample_recipe()

        # When
        res = self.client.delete(recipe_url(recipe_id=recipe.id))

        # Then
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        all_recipes = Recipe.objects.all()
        self.assertEqual(len(all_recipes), 0)

        all_ingredients = Ingredient.objects.all()
        self.assertEqual(len(all_ingredients), 0)

    def test_delete_non_existing_recipe(self):
        """Test deleting an existing recipe that doesn't exist"""
        # Given
        # No recipes defined

        # When
        res = self.client.delete(recipe_url(recipe_id=1))

        # Then
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
