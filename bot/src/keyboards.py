from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⭐ Товары ⭐", callback_data="catalog")],
            [
                InlineKeyboardButton(text="🛒 Корзина", callback_data="cart"),
                InlineKeyboardButton(text="ℹ️ FAQ", callback_data="faq"),
            ],
        ]
    )

    return keyboard


def catalog_keyboard(
    categories: List[str],
    page: int,
    all_pages: int,
    next_id: int = None,
    prev_id: int = None,
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for category in categories:
        category_id = category["id"]
        keyboard.row(
            InlineKeyboardButton(
                text=f"✮ {category['name']} ✮",
                callback_data=f"category_clothes_{category_id}",
            )
        )

    keyboard.row(
        InlineKeyboardButton(text="👈👈 Вернуться в начало", callback_data="start")
    )
    second_row = list()
    if prev_id is not None:
        second_row.append(
            InlineKeyboardButton(text="️⬅", callback_data=f"prev_category_{prev_id}")
        )
    else:
        second_row.append(InlineKeyboardButton(text="🚫", callback_data="none"))
    second_row.append(
        InlineKeyboardButton(text=f"{page}/{all_pages}", callback_data="none")
    )
    if next_id is not None:
        second_row.append(
            InlineKeyboardButton(text="➡", callback_data=f"next_category_{next_id}")
        )
    else:
        second_row.append(InlineKeyboardButton(text="🚫", callback_data="none"))
    keyboard.row(*second_row, width=3)
    return keyboard.as_markup()


def items_pagination_keyboard(
    item_id: int,
    category_id: int,
    page: int,
    all_pages: int,
    next_id: int = None,
    prev_id: int = None,
):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="🛒 Добавить в корзину", callback_data=f"add_cart_item_{item_id}"
        )
    )
    keyboard.row(InlineKeyboardButton(text="👈 Вернуться", callback_data="catalog"))

    second_row = list()
    if prev_id is not None:
        second_row.append(
            InlineKeyboardButton(
                text="⬅", callback_data=f"prev_item_{category_id}_{prev_id}"
            )
        )
    else:
        second_row.append(InlineKeyboardButton(text="🚫", callback_data="none"))
    second_row.append(
        InlineKeyboardButton(text=f"{page}/{all_pages}", callback_data="none")
    )
    if next_id is not None:
        second_row.append(
            InlineKeyboardButton(
                text="️➡", callback_data=f"next_item_{category_id}_{next_id}"
            )
        )
    else:
        second_row.append(InlineKeyboardButton(text="🚫", callback_data="none"))
    keyboard.row(*second_row, width=3)
    return keyboard.as_markup()


def items_cart_pagination_keyboard(
    item_id: int,
    page: int,
    all_pages: int,
    next_id: int = None,
    prev_id: int = None,
):
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        InlineKeyboardButton(text="💵 Сделать заказ 💵", callback_data="buy_items")
    )
    keyboard.row(
        InlineKeyboardButton(text="👈 Вернуться", callback_data="start"),
        InlineKeyboardButton(
            text="➖ Убрать", callback_data=f"delete_item_cart_{item_id}"
        ),
    )

    second_row = list()
    if prev_id is not None:
        second_row.append(
            InlineKeyboardButton(text="⬅", callback_data=f"prev_cart_item_{prev_id}")
        )
    else:
        second_row.append(InlineKeyboardButton(text="🚫", callback_data="none"))
    second_row.append(
        InlineKeyboardButton(text=f"{page}/{all_pages}", callback_data="none")
    )
    if next_id is not None:
        second_row.append(
            InlineKeyboardButton(text="➡", callback_data=f"next_cart_item_{next_id}")
        )
    else:
        second_row.append(InlineKeyboardButton(text="🚫", callback_data="none"))
    keyboard.row(*second_row, width=3)
    return keyboard.as_markup()


def admin_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Сделать рассылку", callback_data="mailing")],
            [InlineKeyboardButton(text="Получить таблицу", callback_data="get_excel")],
        ],
    )
    return keyboard


def mailing_keyboard(mailings):
    keyboard = InlineKeyboardBuilder()
    for mailing in mailings:
        text = mailing["text"][:10] + "..."
        mailing_id = mailing["id"]
        keyboard.row(
            InlineKeyboardButton(text=text, callback_data=f"send_mailing_{mailing_id}")
        )

    return keyboard.as_markup()


def subcribe_keyboard(chat: bool, channel: bool):
    keyboard = InlineKeyboardBuilder()
    if chat:
        keyboard.row(
            InlineKeyboardButton(
                text="Телеграм группа", url="https://t.me/fusion_test_group"
            )
        )
    if channel:
        keyboard.row(
            InlineKeyboardButton(
                text="Телеграм канал", url="https://t.me/fusion_test_channel"
            )
        )

    return keyboard.as_markup()


def confirm_keyboard(count: int):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅", callback_data=f"confirm_{count}"),
                InlineKeyboardButton(text="❌", callback_data="deny"),
            ]
        ]
    )
    return keyboard


def go_to_start():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👈👈 Вернуться в начало", callback_data="start"
                )
            ]
        ]
    )
    return keyboard


def go_to_catalog():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Перейти в каталог", callback_data="catalog")]
        ]
    )
    return keyboard
