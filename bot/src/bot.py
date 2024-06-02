import asyncio
import logging

from create_bot import bot, dp
from routes.admin import admin_router
from routes.buy_items import buy_router
from routes.cart import cart_router
from routes.catalog import catalog_router
from routes.faq import faq_router
from routes.main import main_router


async def main() -> None:
    logging.basicConfig(level=logging.WARNING)

    dp.include_router(main_router)
    dp.include_router(catalog_router)
    dp.include_router(cart_router)
    dp.include_router(admin_router)
    dp.include_router(buy_router)
    dp.include_router(faq_router)

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
