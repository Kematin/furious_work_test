import aiohttp
from aiogram.types import Message
from aiogram.types.input_file import BufferedInputFile
from config import config
from create_bot import bot
from keyboards import subcribe_keyboard

API_HOST = config.API_HOST
previous_messages = {}


async def check_subscribe(message: Message):
    user_id = message.from_user.id
    user_member_group = await bot.get_chat_member(
        chat_id=config.GROUP_ID, user_id=user_id
    )
    user_member_channel = await bot.get_chat_member(
        chat_id=config.CHANNEL_ID, user_id=user_id
    )
    keyboard = False
    match (user_member_group.status == "left", user_member_channel.status == "left"):
        case (True, True):
            keyboard = subcribe_keyboard(True, True)
        case (True, False):
            keyboard = subcribe_keyboard(True, False)
        case (False, True):
            keyboard = subcribe_keyboard(False, True)
    if keyboard:
        await bot.send_message(
            chat_id=user_id,
            text="Похоже вы не подписаны на нас :(",
            reply_markup=keyboard,
        )
        return False
    else:
        return True


async def request_json(url: str):
    headers = {"X-SECRET_KEY": config.X_SECRET_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()


async def post_request(url: str, data):
    headers = {"X-SECRET_KEY": config.X_SECRET_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            return response


async def delete_request(url: str, data):
    headers = {"X-SECRET_KEY": config.X_SECRET_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, json=data, headers=headers) as response:
            return response


async def put_request(url: str, data):
    headers = {"X-SECRET_KEY": config.X_SECRET_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.put(url, json=data, headers=headers) as response:
            return response


async def get_image_request(url: str):
    headers = {"X-SECRET_KEY": config.X_SECRET_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.read()
            else:
                raise ValueError(
                    f"Failed to retrieve file. Status code: {response.status}"
                )


def find_index_by_id(items, item_id):
    for index, item in enumerate(items):
        if item["id"] == item_id:
            return index
    return -1


async def get_image(url, name):
    url = url.split("/")
    url.insert(3, "api")
    url = "/".join(url)
    image_bytes = await get_image_request(url)
    image = BufferedInputFile(image_bytes, filename=f"{name}.png")
    return image


async def delete_message(chat_id: int):
    if chat_id in previous_messages:
        try:
            await bot.delete_message(
                chat_id=chat_id, message_id=previous_messages[chat_id]
            )
        except Exception as e:
            print(f"Error deleting message: {e}")
