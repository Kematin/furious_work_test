import os
from functools import wraps

from django.http import Http404, HttpResponse
from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.config import config
from clothes.models.clothes import Category, CategoryClothes, Clothes
from clothes.serializers.clothes import (
    CategoryClothesSerializer,
    CategorySerializer,
    ClothesSerializer,
)


def check_secret_key(func):
    @wraps(func)
    def wrapped(self, request, *args, **kwargs):
        secret_key = request.headers.get("X-SECRET-KEY")
        if secret_key != config.X_SECRET_KEY:
            return Response(
                {"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return func(self, request, *args, **kwargs)

    return wrapped


class BaseView(mixins.ListModelMixin, GenericAPIView):
    # @check_secret_key
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ClothesView(BaseView):
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer

    def get(self, request, *args, **kwargs):
        category_id = request.query_params.get("category_id")
        queryset = self.get_queryset()
        if category_id is not None:
            queryset = queryset.filter(category=category_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ClothesSingleView(RetrieveUpdateAPIView):
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer

    def put(self, request, *args, **kwargs):
        kwargs["partial"] = True
        instance = self.get_object()
        sent_count = self.request.data.get("counts", 0)
        try:
            sent_count = int(sent_count)
        except ValueError:
            return Response(
                {"error": "Invalid count value"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Subtract the sent count from the instance count
        instance.counts = instance.counts - sent_count

        # Save the instance with the updated count
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ClothesMediaView(APIView):
    def get(self, request, *args, **kwargs):
        img_name = kwargs.get("url")
        if not img_name:
            return HttpResponse(status=400)

        file_path = os.path.join("clothes/media", img_name)

        if not os.path.exists(file_path):
            file_path = os.path.join("clothes/media/items", img_name)
            if not os.path.exists(file_path):
                raise Http404("Image not found")

        with open(file_path, "rb") as image_file:
            return HttpResponse(image_file.read(), content_type="image/jpeg")


class CategoryView(BaseView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryClothesView(BaseView):
    queryset = CategoryClothes.objects.all()
    serializer_class = CategoryClothesSerializer

    def get(self, request, *args, **kwargs):
        category_id = kwargs.get("category_id")
        queryset = self.get_queryset().filter(main_category=category_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
