import csv
import os

import pandas as pd
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.types.input_file import FSInputFile
from config import config
from create_bot import bot
from keyboards import admin_keyboard, mailing_keyboard
from service import (
    API_HOST,
    delete_message,
    previous_messages,
    request_json,
)

admin_router = Router()


@admin_router.message(Command("admin"))
async def admin_panel(message: Message):
    user_id = message.from_user.id
    url = API_HOST + f"api/mailing/{user_id}"
    response = await request_json(url)
    await delete_message(chat_id=user_id)
    if isinstance(response, list):
        keyboard = admin_keyboard()
        message = await bot.send_message(
            chat_id=user_id, text="Добро пожаловать", reply_markup=keyboard
        )
        previous_messages[user_id] = message.message_id
    else:
        message = await bot.send_message(chat_id=user_id, text="Доступ заблокирован")
        previous_messages[user_id] = message.message_id


@admin_router.callback_query(lambda c: c.data == "mailing")
async def mailing(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    url = API_HOST + f"api/mailing/{user_id}/"
    mailings = await request_json(url)
    keyboard = mailing_keyboard(mailings=mailings)
    await delete_message(chat_id=user_id)
    message = await bot.send_message(
        chat_id=user_id, text="Выберите рассылку", reply_markup=keyboard
    )
    previous_messages[user_id] = message.message_id


@admin_router.callback_query(lambda c: c.data.startswith("send_mailing_"))
async def send_mailing(callback_query: CallbackQuery):
    mailing_id = callback_query.data.split("_")[-1]
    user_id = callback_query.from_user.id
    mailing = await request_json(API_HOST + f"api/mailing/{user_id}/{mailing_id}/")
    url = API_HOST + f"api/users/all/{user_id}/"
    users = await request_json(url)
    for data in users:
        user = data["user_id"]
        if str(user_id) == user:
            continue
        await bot.send_message(chat_id=user, text=mailing["text"])

    await delete_message(chat_id=user_id)
    message = await bot.send_message(chat_id=user_id, text="Рассылки выполнены успешно")
    previous_messages[user_id] = message.message_id


@admin_router.callback_query(lambda c: c.data == "get_excel")
async def get_excel(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    await delete_message(chat_id=user_id)
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
    df = pd.read_csv(csv_file)
    df.to_excel(config.TABLE_FILENAME + ".xlsx", index=False)
    document = FSInputFile(config.TABLE_FILENAME + ".xlsx")
    await bot.send_document(chat_id=user_id, document=document)
