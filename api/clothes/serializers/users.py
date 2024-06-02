from rest_framework import serializers

from clothes.models.users import Cart, Mailing, TelegramUser


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = "__all__"


class UsersIdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ["user_id"]


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
