from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from create_bot import bot
from service import (
    check_subscribe,
    delete_message,
    previous_messages,
)

faq_router = Router()

start_button = InlineKeyboardButton(
    text="👈👈 Вернуться в начало", callback_data="start"
)
faq_button = InlineKeyboardButton(text="👈 Вернуться к вопросам", callback_data="faq")

go_to_faq = InlineKeyboardMarkup(
    inline_keyboard=[
        [faq_button],
        [start_button],
    ]
)


async def handle_faq(user_id: int):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎯 Гарантия", callback_data="faq_guarantee")],
            [InlineKeyboardButton(text="🚗 Доставка", callback_data="faq_shipping")],
            [InlineKeyboardButton(text="💯 Качество", callback_data="faq_quality")],
            [start_button],
        ]
    )

    await delete_message(chat_id=user_id)
    message = await bot.send_message(
        chat_id=user_id, text="Популярные темы вопросов:", reply_markup=keyboard
    )
    previous_messages[user_id] = message.message_id


@faq_router.message(Command("faq"))
async def faq_command(message: Message):
    if await check_subscribe(message=message):
        await handle_faq(message.from_user.id)


@faq_router.callback_query(lambda c: c.data == "faq")
async def faq_query(callback_query: CallbackQuery):
    if await check_subscribe(message=callback_query):
        await handle_faq(callback_query.from_user.id)


@faq_router.callback_query(lambda c: c.data == "faq_shipping")
async def faq_shipping(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    await delete_message(user_id)
    message = await bot.send_message(
        chat_id=user_id,
        text="<b>Доставка осущствляется только по России!!!</b>\n\nМы доставляем <b>Почтой России</b> по цене в 30 рублей :)",
        reply_markup=go_to_faq,
    )
    previous_messages[user_id] = message.message_id


@faq_router.callback_query(lambda c: c.data == "faq_guarantee")
async def faq_guarantee(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    await delete_message(user_id)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎯 Гарантия товара", callback_data="faq_guarantee_item"
                )
            ],
            [
                InlineKeyboardButton(
                    text="♻ Возврат товара", callback_data="faq_guarantee_refund"
                )
            ],
            [faq_button],
        ]
    )

    message = await bot.send_message(
        chat_id=user_id, text="Выберите интересующий вас вопрос:", reply_markup=keyboard
    )
    previous_messages[user_id] = message.message_id


@faq_router.callback_query(lambda c: c.data.startswith("faq_guarantee_"))
async def faq_guarantity_sub(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    await delete_message(chat_id=user_id)
    data = callback_query.data.split("_")[-1]

    if data == "item":
        message = await bot.send_message(
            chat_id=user_id, text="Гарантия товара 1 год", reply_markup=go_to_faq
        )
    else:
        message = await bot.send_message(
            chat_id=user_id,
            text="Возврат осуществляется через нашего менджера\n\nЕсли ваш товар был поврежден в ходе доставки, вы можете написать ему по данному вопросу",
            reply_markup=go_to_faq,
        )

    previous_messages[user_id] = message.message_id


@faq_router.callback_query(lambda c: c.data == "faq_quality")
async def faq_quality(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    await delete_message(user_id)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🧶 Материалы", callback_data="faq_quality_material"
                )
            ],
            [faq_button],
        ]
    )

    message = await bot.send_message(
        chat_id=user_id, text="Выберите интересующий вас вопрос:", reply_markup=keyboard
    )
    previous_messages[user_id] = message.message_id


@faq_router.callback_query(lambda c: c.data == "faq_quality_material")
async def faq_quantity_sub(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    await delete_message(chat_id=user_id)

    message = await bot.send_message(
        chat_id=user_id,
        text="Материалы нашей одежды:\n1. Хлопок\n2. Лен\n3. Шелк\n4. Шерсть",
        reply_markup=go_to_faq,
    )
    previous_messages[user_id] = message.message_id
