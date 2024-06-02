from django.urls import path

from clothes.views.clothes import (
    CategoryClothesView,
    CategoryView,
    ClothesMediaView,
    ClothesSingleView,
    ClothesView,
)
from clothes.views.users import (
    CartAddView,
    CartView,
    MailingView,
    UserCreateView,
    UserIdsView,
)

urlpatterns = [
    path("category/", CategoryView.as_view(), name="основные категории"),
    path(
        "category_clothes/<int:category_id>/",
        CategoryClothesView.as_view(),
        name="категории одежды",
    ),
    path("clothes/", ClothesView.as_view(), name="одежда"),
    path("clothes/<int:pk>/", ClothesSingleView.as_view(), name="одна вещь"),
    path(
        "clothes/media/<str:url>/",
        ClothesMediaView.as_view(),
        name="получить изображение",
    ),
    path(
        "clothes/media/items/<str:url>/",
        ClothesMediaView.as_view(),
        name="получить изображение",
    ),
    path("users/", UserCreateView.as_view(), name="добавление пользователя"),
    path(
        "users/all/<str:user_id>/",
        UserIdsView.as_view(),
        name="получение айди пользователей",
    ),
    path(
        "cart/",
        CartAddView.as_view(),
        name="Добавление вещи в корзину",
    ),
    path(
        "cart/<str:user_id>/",
        CartView.as_view(),
        name="получение корзины",
    ),
    path("mailing/<str:user_id>/", MailingView.as_view(), name="получение рассылок"),
    path(
        "mailing/<str:user_id>/<int:pk>/",
        MailingView.as_view(),
        name="получение определенной рассылки",
    ),
]
