from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from clothes.models.clothes import Clothes
from clothes.models.users import Cart, Mailing, TelegramUser
from clothes.serializers.clothes import ClothesSerializer
from clothes.serializers.users import (
    CartSerializer,
    MailingSerializer,
    UsersIdsSerializer,
    UsersSerializer,
)


class CartAddView(mixins.CreateModelMixin, GenericAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = (
            self.get_queryset()
            .filter(user=request.data["user"])
            .filter(clothes=request.data["clothes"])
        )
        if instance.exists():
            return Response(
                {"detail": "Item already in cart"}, status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class CartView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        queryset = self.get_queryset().filter(user=user_id)
        serializer = self.get_serializer(queryset, many=True)
        for i, item in enumerate(serializer.data):
            serializer.data[i]["clothes"] = ClothesSerializer(
                Clothes.objects.get(id=item["clothes"])
            ).data
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        clothes_id = int(request.data["item_id"])
        instance = self.get_queryset().filter(user=user_id).filter(clothes=clothes_id)

        if instance.exists():
            instance.delete()
            return Response({"detail": "successful"})
        else:
            return Response({"detail": "Not found"}, status=404)


class UserCreateView(mixins.CreateModelMixin, GenericAPIView):
    queryset = TelegramUser.objects.all()
    serializer_class = UsersSerializer

    def post(self, request, *args, **kwargs):
        # TODO CHECK SECRET KEY
        return self.create(request, *args, **kwargs)


class UserCart(GenericAPIView):
    queryset = TelegramUser.objects.all()
    serializer_class = UsersSerializer

    def _check_exist(self, user_id: int, cart_id: int):
        if not user_id:
            return Response(
                {"detail": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not cart_id:
            return Response(
                {"detail": "Cart ID not provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = self.queryset.get(user_id=user_id)
        except TelegramUser.DoesNotExist:
            return Response(
                {"detail": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            cart_item = Clothes.objects.get(id=cart_id)
        except Clothes.DoesNotExist:
            return Response(
                {"detail": "Cart item does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        return user, cart_item

    def get(self, request, *args, **kwargs):
        # TODO CHECK SECRET KEY
        user_id = kwargs.get("user_id")
        if not user_id:
            return Response(
                {"detail": "Username not provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = self.queryset.get(user_id=user_id)
            serializer = self.serializer_class(user)
            cart_ids = serializer.data["cart"]
            cart = [Clothes.objects.get(id=cart_id) for cart_id in cart_ids]
            return Response(ClothesSerializer(cart, many=True).data)
        except TelegramUser.DoesNotExist:
            return Response(
                {"detail": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        cart_id = request.data.get("cart_id")

        user, cart_item = self._check_exist(user_id=user_id, cart_id=cart_id)

        if user.cart.filter(id=cart_id).exists():
            return Response(
                {"detail": "Item already in cart"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            user.cart.add(cart_item)
            return Response({"detail": "Item added to cart"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        user_id = int(kwargs.get("user_id"))
        cart_id = request.data.get("cart_id")

        user, cart_item = self._check_exist(user_id=user_id, cart_id=cart_id)

        if user.cart.filter(id=cart_id).exists():
            user.cart.remove(cart_item)
            return Response(
                {"detail": "Item removed from cart"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "No item in cart"}, status=status.HTTP_400_BAD_REQUEST
            )


class MailingView(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def get(self, request, *args, **kwargs):
        # TODO CHECK SECRET KEY
        user_id = kwargs.get("user_id")
        pk = kwargs.get("pk")
        try:
            user = TelegramUser.objects.all().get(user_id=user_id)
            if user.is_admin:
                if pk is None:
                    return self.list(request, *args, **kwargs)
                else:
                    return self.retrieve(request)
            else:
                return Response(
                    {"detail": "Unauthorized."}, status=status.HTTP_400_BAD_REQUEST
                )
        except TelegramUser.DoesNotExist:
            return Response(
                {"detail": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST
            )


class UserIdsView(mixins.ListModelMixin, GenericAPIView):
    queryset = TelegramUser.objects.all()
    serializer_class = UsersIdsSerializer

    def get(self, request, *args, **kwargs):
        # TODO CHECK SECRET KEY
        user_id = kwargs.get("user_id")
        try:
            user = TelegramUser.objects.all().get(user_id=user_id)
            if user.is_admin:
                return self.list(request, *args, **kwargs)
            else:
                return Response(
                    {"detail": "Unauthorized."}, status=status.HTTP_400_BAD_REQUEST
                )
        except TelegramUser.DoesNotExist:
            return Response(
                {"detail": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST
            )
