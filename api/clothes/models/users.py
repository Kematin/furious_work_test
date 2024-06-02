from django.core.validators import MinValueValidator
from django.db import models

from clothes.models.clothes import Clothes


class TelegramUser(models.Model):
    user_id = models.CharField(primary_key=True, max_length=20)
    username = models.CharField(unique=True, max_length=150)
    is_admin = models.BooleanField(default=False, blank=True)

    def __str__(self) -> str:
        return self.username


class Mailing(models.Model):
    text = models.TextField()

    def __str__(self) -> str:
        return f"{self.text[:20]}..."


class Cart(models.Model):
    user = models.ForeignKey(to=TelegramUser, on_delete=models.CASCADE)
    clothes = models.ForeignKey(to=Clothes, on_delete=models.CASCADE)
    counts = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.user} | {self.clothes} | COUNT {self.counts}"
