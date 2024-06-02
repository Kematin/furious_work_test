from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from config import config
from create_bot import bot
from descriptions import make_category_description, make_item_description
from keyboards import (
    catalog_keyboard,
    go_to_catalog,
    go_to_start,
    items_pagination_keyboard,
)
from service import (
    check_subscribe,
    delete_message,
    find_index_by_id,
    get_image,
    previous_messages,
    request_json,
)

catalog_router = Router()


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


async def handle_catalog_pagination(chat_id: int, category_id: int, main_categories):
    prev_id, next_id = None, None
    url = config.API_HOST + f"api/category_clothes/{category_id}/"
    categories = await request_json(url)
    index = find_index_by_id(main_categories, category_id)
    name, desc = main_categories[index]["name"], main_categories[index]["description"]
    if index > 0:
        prev_id = main_categories[index - 1]["id"]
    if index < len(main_categories) - 1:
        next_id = main_categories[index + 1]["id"]

    keyboard = catalog_keyboard(
        categories=categories,
        prev_id=prev_id,
        next_id=next_id,
        page=index + 1,
        all_pages=len(main_categories),
    )

    image_url = main_categories[index]["imageUrl"]
    image = await get_image(image_url, name)

    await delete_message(chat_id=chat_id)

    sent_message = await bot.send_photo(
        chat_id=chat_id,
        photo=image,
        caption=make_category_description(name, desc),
        reply_markup=keyboard,
    )
    previous_messages[chat_id] = sent_message.message_id


async def handle_catalog(chat_id: int):
    url = config.API_HOST + "api/category/"
    main_categories = await request_json(url)
    if len(main_categories) < 1:
        await bot.send_message(
            chat_id=chat_id,
            text="Пока нет товаров :(",
            reply_markup=go_to_start(),
        )
    else:
        first_id = main_categories[0]["id"]
        await handle_catalog_pagination(
            chat_id=chat_id,
            category_id=first_id,
            main_categories=main_categories,
        )


@catalog_router.message(Command("catalog"))
async def catalog_command(message: Message) -> None:
    if await check_subscribe(message):
        await handle_catalog(message.from_user.id)


@catalog_router.callback_query(lambda c: c.data == "catalog")
async def catalog_button(callback_query: CallbackQuery) -> None:
    if await check_subscribe(callback_query):
        await handle_catalog(callback_query.from_user.id)


@catalog_router.callback_query(lambda c: c.data.startswith("prev_category_"))
async def prev_category(callback_query: CallbackQuery) -> None:
    url = config.API_HOST + "api/category/"
    main_categories = await request_json(url)
    prev_category_id = int(callback_query.data.split("_")[-1])
    await handle_catalog_pagination(
        chat_id=callback_query.from_user.id,
        category_id=prev_category_id,
        main_categories=main_categories,
    )


@catalog_router.callback_query(lambda c: c.data.startswith("next_category_"))
async def next_category(callback_query: CallbackQuery) -> None:
    url = config.API_HOST + "api/category/"
    main_categories = await request_json(url)
    next_category_id = int(callback_query.data.split("_")[-1])
    await handle_catalog_pagination(
        chat_id=callback_query.from_user.id,
        category_id=next_category_id,
        main_categories=main_categories,
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


async def handler_items_pagination(chat_id, category_id, item_id):
    prev_id, next_id = None, None
    url = config.API_HOST + f"/api/clothes/?category_id={category_id}"
    items = await request_json(url)
    index = find_index_by_id(items, item_id)
    name = items[index]["name"]
    if index > 0:
        prev_id = items[index - 1]["id"]
    if index < len(items) - 1:
        next_id = items[index + 1]["id"]

    keyboard = items_pagination_keyboard(
        item_id=item_id,
        category_id=category_id,
        prev_id=prev_id,
        next_id=next_id,
        page=index + 1,
        all_pages=len(items),
    )

    image_url = items[index]["imageUrl"]
    image = await get_image(image_url, name)

    await delete_message(chat_id=chat_id)

    sent_message = await bot.send_photo(
        chat_id=chat_id,
        photo=image,
        caption=make_item_description(items[index]),
        reply_markup=keyboard,
    )
    previous_messages[chat_id] = sent_message.message_id


@catalog_router.callback_query(lambda c: c.data.startswith("category_clothes_"))
async def get_category_clothes(callback_query: CallbackQuery):
    category_id = int(callback_query.data.split("_")[-1])
    chat_id = callback_query.from_user.id
    url = config.API_HOST + f"/api/clothes/?category_id={category_id}"
    items = await request_json(url)
    if len(items) < 1:
        await delete_message(chat_id=chat_id)
        message = await bot.send_message(
            chat_id=chat_id,
            text="Пока нет товаров по данной категории :(",
            reply_markup=go_to_catalog(),
        )
        previous_messages[chat_id] = message.message_id
    else:
        await delete_message(chat_id=chat_id)
        first_id = items[0]["id"]
        await handler_items_pagination(
            chat_id=chat_id, category_id=category_id, item_id=first_id
        )


@catalog_router.callback_query(lambda c: c.data.startswith("prev_item_"))
async def prev_item(callback_query: CallbackQuery) -> None:
    prev_item_id = int(callback_query.data.split("_")[-1])
    category_id = int(callback_query.data.split("_")[-2])
    await handler_items_pagination(
        chat_id=callback_query.from_user.id,
        category_id=category_id,
        item_id=prev_item_id,
    )


@catalog_router.callback_query(lambda c: c.data.startswith("next_item_"))
async def next_item(callback_query: CallbackQuery) -> None:
    next_item_id = int(callback_query.data.split("_")[-1])
    category_id = int(callback_query.data.split("_")[-2])
    await handler_items_pagination(
        chat_id=callback_query.from_user.id,
        category_id=category_id,
        item_id=next_item_id,
    )
