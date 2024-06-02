from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from create_bot import bot
from descriptions import make_cart_description
from keyboards import confirm_keyboard, go_to_start, items_cart_pagination_keyboard
from service import (
    API_HOST,
    check_subscribe,
    delete_message,
    delete_request,
    get_image,
    post_request,
    previous_messages,
    request_json,
)

cart_router = Router()


def find_index_by_id(items, item_id):
    for index, item in enumerate(items):
        if item["clothes"]["id"] == item_id:
            return index
    return -1


async def handler_items_pagination(user_id, item_id):
    prev_id, next_id = None, None
    url = API_HOST + f"api/cart/{user_id}/"
    items = await request_json(url)
    index = find_index_by_id(items, item_id)
    name = items[index]["clothes"]["name"]

    if index > 0:
        prev_id = items[index - 1]["clothes"]["id"]
    if index < len(items) - 1:
        next_id = items[index + 1]["clothes"]["id"]

    keyboard = items_cart_pagination_keyboard(
        item_id=item_id,
        page=index + 1,
        all_pages=len(items),
        next_id=next_id,
        prev_id=prev_id,
    )

    image_url = API_HOST + items[index]["clothes"]["imageUrl"][1:]
    image = await get_image(image_url, name)

    await delete_message(chat_id=user_id)

    sent_message = await bot.send_photo(
        chat_id=user_id,
        photo=image,
        caption=make_cart_description(items[index]),
        reply_markup=keyboard,
    )
    previous_messages[user_id] = sent_message.message_id


async def handler_get_cart(user_id):
    url = API_HOST + f"api/cart/{user_id}/"
    items = await request_json(url)
    if len(items) < 1:
        await delete_message(chat_id=user_id)
        message = await bot.send_message(
            chat_id=user_id, text="У вас пустая корзина :(", reply_markup=go_to_start()
        )
        previous_messages[user_id] = message.message_id
    else:
        await delete_message(chat_id=user_id)
        first_id = items[0]["clothes"]["id"]
        await handler_items_pagination(user_id=user_id, item_id=first_id)


@cart_router.message(Command("cart"))
async def get_cart_command(message: Message):
    if await check_subscribe(message):
        await handler_get_cart(message.from_user.id)


@cart_router.callback_query(lambda c: c.data == "cart")
async def get_cart_query(callback_query: CallbackQuery):
    if await check_subscribe(callback_query):
        await handler_get_cart(callback_query.from_user.id)


@cart_router.callback_query(lambda c: c.data.startswith("prev_cart_item_"))
async def prev_item(callback_query: CallbackQuery) -> None:
    prev_item_id = int(callback_query.data.split("_")[-1])
    await handler_items_pagination(
        user_id=callback_query.from_user.id,
        item_id=prev_item_id,
    )


@cart_router.callback_query(lambda c: c.data.startswith("next_cart_item_"))
async def next_item(callback_query: CallbackQuery) -> None:
    next_item_id = int(callback_query.data.split("_")[-1])
    await handler_items_pagination(
        user_id=callback_query.from_user.id,
        item_id=next_item_id,
    )


##################################################
##################################################
##################################################
##################################################
##################################################
##################################################
##################################################
##################################################
##################################################
##################################################


async def handle_delete_item(user_id, item_id):
    data = {"item_id": item_id}
    url = API_HOST + f"api/cart/{user_id}/"
    await delete_request(url=url, data=data)
    await delete_message(chat_id=user_id)


@cart_router.callback_query(lambda c: c.data.startswith("delete_item_cart_"))
async def delete_item(callback_query: CallbackQuery) -> None:
    item_id = int(callback_query.data.split("_")[-1])
    user_id = callback_query.from_user.id
    await handle_delete_item(user_id=user_id, item_id=item_id)
    await get_cart_query(callback_query)


class AddToCart(StatesGroup):
    choose_count = State()
    confirm = State()


item_ids = {}


@cart_router.callback_query(
    StateFilter(None), lambda c: c.data.startswith("add_cart_item_")
)
async def add_item(callback_query: CallbackQuery, state: FSMContext):
    item_id = int(callback_query.data.split("_")[-1])
    user_id = callback_query.from_user.id
    item_ids[user_id] = item_id
    await delete_message(chat_id=user_id)
    message = await bot.send_message(chat_id=user_id, text="Напишите количество:")
    previous_messages[user_id] = message.message_id
    await state.set_state(AddToCart.choose_count)


@cart_router.message(AddToCart.choose_count)
async def choose_count_item(message: Message, state: FSMContext):
    user_id = message.from_user.id
    item_id = item_ids[user_id]
    item = await request_json(API_HOST + f"api/clothes/{item_id}/")
    counts = message.text.lower()
    if not counts.isdigit():
        await delete_message(chat_id=user_id)
        message = await bot.send_message(chat_id=user_id, text="Напишите количество:")
        previous_messages[user_id] = message.message_id
        await state.set_state(AddToCart.choose_count)
    elif int(counts) > item["counts"]:
        await delete_message(chat_id=user_id)
        message = await bot.send_message(
            chat_id=user_id, text="Вы выбрали больше доступного:"
        )
        previous_messages[user_id] = message.message_id
        await state.set_state(AddToCart.choose_count)
    elif int(counts) < 1:
        await delete_message(chat_id=user_id)
        message = await bot.send_message(
            chat_id=user_id, text="Вы выбрали неправильное число:"
        )
        previous_messages[user_id] = message.message_id
        await state.set_state(AddToCart.choose_count)
    else:
        await delete_message(chat_id=user_id)
        keyboard = confirm_keyboard(count=int(counts))
        message = await bot.send_message(
            chat_id=user_id, text="Подтвердите свой выбор", reply_markup=keyboard
        )
        previous_messages[user_id] = message.message_id
        await state.set_state(AddToCart.confirm)


@cart_router.callback_query(AddToCart.confirm)
async def confirm_add_item(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    data = callback_query.data
    if data.startswith("confirm"):
        counts = int(callback_query.data.split("_")[-1])
        item_id = item_ids[user_id]
        data = {"user": user_id, "clothes": item_id, "counts": counts}
        url = API_HOST + "api/cart/"
        await post_request(url=url, data=data)
        await delete_message(chat_id=user_id)
        await get_cart_query(callback_query)
        del item_ids[user_id]
    else:
        await delete_message(chat_id=user_id)
        await get_cart_query(callback_query)

    await state.clear()
