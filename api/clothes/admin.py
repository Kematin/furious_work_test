from django.contrib import admin

from clothes.models.clothes import Category, CategoryClothes, Clothes
from clothes.models.users import Cart, Mailing, TelegramUser

# Register your models here.
admin.site.register(Category)
admin.site.register(Clothes)
admin.site.register(CategoryClothes)
admin.site.register(TelegramUser)
admin.site.register(Mailing)
admin.site.register(Cart)
