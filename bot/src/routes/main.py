from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from create_bot import bot
from descriptions import WELCOME_TEXT
from keyboards import start_keyboard
from service import (
    API_HOST,
    check_subscribe,
    delete_message,
    post_request,
    previous_messages,
)

main_router = Router()


async def handler_start(user_id: int, username: str):
    url = API_HOST + "api/users/"
    data = {"user_id": user_id, "username": username}
    response = await post_request(url=url, data=data)
    if response.status == 201:
        await delete_message(chat_id=user_id)
        message = await bot.send_message(
            chat_id=user_id, text=WELCOME_TEXT, reply_markup=start_keyboard()
        )
        previous_messages[user_id] = message.message_id
    else:
        await delete_message(chat_id=user_id)
        message = await bot.send_message(
            chat_id=user_id, text=WELCOME_TEXT, reply_markup=start_keyboard()
        )
        previous_messages[user_id] = message.message_id


@main_router.message(Command("start"))
async def start(message: Message) -> None:
    user_id, username = message.from_user.id, message.from_user.username
    if await check_subscribe(message):
        await handler_start(user_id=user_id, username=username)


@main_router.callback_query(lambda c: c.data == "start")
async def start_query(callback_query: CallbackQuery):
    user_id, username = callback_query.from_user.id, callback_query.from_user.username
    if await check_subscribe(callback_query):
        await handler_start(user_id=user_id, username=username)


@main_router.callback_query(lambda c: c.data == "none")
async def handle_none(_: CallbackQuery):
    print("none")
