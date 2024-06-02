WELCOME_TEXT = (
    "👋 Добро пожаловать в <b>Fusion</b> – ваш магазин стильной одежды!\n\n"
    "✨ Здесь вы найдете самые последние тренды и коллекции.\n\n"
    "🛍️ С нами шоппинг становится проще!\n\n"
    "📲 Используйте команды ниже, чтобы начать:\n"
    "/catalog – Просмотреть каталог\n"
    "/cart – Ваша корзина \n"
    "/faq – Часто задаваемые вопросы\n\n"
    "Если у вас есть вопросы, не стесняйтесь обращаться к нашей поддержке.\n\n"
    "Приятных покупок! 🎉"
)


def make_category_description(name, desc):
    category_text = f"<b>{name}</b>\n\n" + desc
    return category_text


def make_item_description(item):
    name, counts, price, desc = (
        item["name"],
        item["counts"],
        item["price"],
        item["description"],
    )
    desc_text = (
        f"<b>{name}</b>\n\n"
        + desc
        + "\n\n"
        + f"Количество: {counts}\n"
        + f"Цена: <b>{price}</b>"
    )
    return desc_text


def make_cart_description(item):
    name, counts, price, desc = (
        item["clothes"]["name"],
        item["counts"],
        item["clothes"]["price"] * item["counts"],
        item["clothes"]["description"],
    )
    desc_text = (
        f"<b>{name}</b>\n\n"
        + desc
        + "\n\n"
        + f"Количество: {counts}\n"
        + f"Общая сумма: <b>{price}</b>"
    )
    return desc_text
