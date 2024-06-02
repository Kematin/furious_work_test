import csv
import os

from aiogram import F, Router
from aiogram.types import (
    CallbackQuery,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
    ShippingOption,
    ShippingQuery,
)
from config import config
from create_bot import bot
from keyboards import go_to_start
from routes.cart import handle_delete_item
from service import (
    API_HOST,
    put_request,
    request_json,
)

buy_router = Router()


RU_SHIPPING = ShippingOption(
    id="ru",
    title="Доставка по России",
    prices=[
        LabeledPrice(label="Доставка почтой России", amount=1000),
        LabeledPrice(label="Доставка СДЭК", amount=2000),
    ],
)


async def add_to_excel(user_id, username, items):
    csv_file = config.TABLE_FILENAME + ".csv"
    file_exists = os.path.isfile(csv_file)
    if not file_exists:
        with open(csv_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(
                    [
                        "user_id",
                        "Имя пользователя",
                        "Название товара",
                        "Количество",
                        "Сумма",
                    ]
                )
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)

        for item in items:
            name = item["clothes"]["name"]
            counts = item["counts"]
            total_price = item["clothes"]["price"] * counts
            writer.writerow([user_id, username, name, counts, total_price])


async def handle_successfull_payment(message: Message):
    user_id = message.from_user.id
    url = API_HOST + f"api/cart/{user_id}/"
    items = await request_json(url)
    for item in items:
        item_id = item["clothes"]["id"]
        data = {"counts": item["counts"]}
        await put_request(API_HOST + f"api/clothes/{item_id}/", data=data)
        await handle_delete_item(user_id=user_id, item_id=item_id)

    await add_to_excel(
        user_id=user_id, username=message.from_user.username, items=items
    )
    keyboard = go_to_start()
    await bot.send_message(
        user_id, text="Оплата выполнена успешно!", reply_markup=keyboard
    )


@buy_router.callback_query(lambda c: c.data == "buy_items")
async def buy_items(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    url = API_HOST + f"api/cart/{user_id}/"
    cart_items = await request_json(url)
    total_sum = 0
    for item in cart_items:
        total_sum += item["counts"] * item["clothes"]["price"]
    title = " | ".join(
        [f'{item["clothes"]["name"]} ({item["counts"]}x)' for item in cart_items]
    )
    await bot.send_message(
        chat_id=user_id, text="ТЕСТОВЫЙ ПЛАТЕЖ НЕ БОЛЬШЕ 1000 РУБЛЕЙ!"
    )

    await bot.send_invoice(
        chat_id=user_id,
        title=title,
        description="Спасибо за покупку :)",
        payload="q",
        provider_token=config.PAYMENT_TOKEN,
        currency="rub",
        prices=[LabeledPrice(label="Заказ одежды", amount=total_sum * 100)],
        max_tip_amount=50000,
        suggested_tip_amounts=[5000, 10000, 30000],
        need_name=True,
        need_phone_number=True,
        need_email=False,
        need_shipping_address=True,
        is_flexible=True,
        request_timeout=15,
    )


@buy_router.shipping_query(lambda q: True)
async def shipping_check(query: ShippingQuery):
    user_id = query.id
    shipping_options = []
    print(query.shipping_address.country_code)
    if query.shipping_address.country_code not in ["RU", "AD"]:
        return await bot.answer_shipping_query(
            shipping_query_id=user_id,
            ok=False,
            error_message="Доставка в выбранную страну не осуществляется",
        )
    else:
        shipping_options.append(RU_SHIPPING)

    await bot.answer_shipping_query(
        shipping_query_id=user_id, ok=True, shipping_options=shipping_options
    )


@buy_router.pre_checkout_query(lambda q: True)
async def pre_check_query(query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, ok=True)


@buy_router.message(F.successful_payment)
async def successfull_payment(message: Message):
    await handle_successfull_payment(message)
