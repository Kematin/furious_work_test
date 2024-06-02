from rest_framework import serializers

from clothes.models.clothes import Category, CategoryClothes, Clothes


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryClothes
        fields = "__all__"


class ClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = "__all__"

        extra_kwargs = {
            "name": {"required": False},
            "description": {"required": False},
            "price": {"required": False},
            "imageUrl": {"required": False},
            "category": {"required": False},
        }
