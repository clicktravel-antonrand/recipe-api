from django.db import models


class Recipe(models.Model):
    """Recipe Model"""
    name = models.TextField(blank=False)
    description = models.TextField()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used for a recipe"""
    name = models.TextField(blank=False)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )

    def __str__(self):
        return self.name
