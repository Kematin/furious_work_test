from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    imageUrl = models.ImageField(unique=True, upload_to="clothes/media")
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class CategoryClothes(models.Model):
    name = models.CharField(max_length=100)
    main_category = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.main_category}, {self.name}"


class Clothes(models.Model):
    name = models.CharField(max_length=150)
    counts = models.IntegerField(validators=[MinValueValidator(0)])
    price = models.IntegerField(validators=[MinValueValidator(100)])
    description = models.TextField()
    imageUrl = models.ImageField(unique=True, upload_to="clothes/media/items")
    category = models.ForeignKey(to=CategoryClothes, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.category}: {self.name}"
