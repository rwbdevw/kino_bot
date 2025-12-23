from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

inlinekeyboard = InlineKeyboardMarkup()
inlinekeyboard.add(InlineKeyboardButton(text="🆕 Yangiliklar", callback_data="news_menu"),
InlineKeyboardButton(text="🚀 Mashhur", callback_data="popular_menu"))
inlinekeyboard.add(InlineKeyboardButton(text="🔍 Qidirish", callback_data="poisk"),
InlineKeyboardButton(text="🎞️ To‘plamlar", callback_data="collections"))
inlinekeyboard.add(InlineKeyboardButton(text="⭐ Sevimlilarim", callback_data="favorites"))
inlinekeyboard.add(InlineKeyboardButton(text="💡 Bot haqida", callback_data="about"),
InlineKeyboardButton(text="💬 Aloqa", callback_data="contacts"))

news_menu_kb = InlineKeyboardMarkup()
news_menu_kb.add(InlineKeyboardButton(text="Filmlar", callback_data="news_films"), InlineKeyboardButton(text="Seriallar", callback_data="news_serials"))
news_menu_kb.add(InlineKeyboardButton(text="TV-shou", callback_data="news_show"))
news_menu_kb.add(InlineKeyboardButton(text="◀️ Orqaga", callback_data="back"))

popular_menu_kb = InlineKeyboardMarkup()
popular_menu_kb.add(InlineKeyboardButton(text="Filmlar", callback_data="popular_films"), InlineKeyboardButton(text="Seriallar", callback_data="popular_series"))
popular_menu_kb.add(InlineKeyboardButton(text="Multfilmlar", callback_data="popular_cartoon"), InlineKeyboardButton(text="Multseriallar", callback_data="popular_cartoon_serials"))
popular_menu_kb.add(InlineKeyboardButton(text="Anime filmlar", callback_data="popular_anime"), InlineKeyboardButton(text="Anime seriallar", callback_data="popular_anime_serials"))
popular_menu_kb.add(InlineKeyboardButton(text="TV-shou", callback_data="popular_show"))
popular_menu_kb.add(InlineKeyboardButton(text="◀️ Orqaga", callback_data="back"))

inlinekeyboard2 = InlineKeyboardMarkup()
inlinekeyboard2.add(InlineKeyboardButton(text="◀️ Kategoriyalar", callback_data="categories"),
InlineKeyboardButton(text="🏠 Menyu", callback_data="back"))

inlinekeyboard3 = InlineKeyboardMarkup()
inlinekeyboard3.add(InlineKeyboardButton(text="◀️ Kategoriyalar", callback_data="categories"),
InlineKeyboardButton(text="🏠 Menyu", callback_data="back"))

inlinekeyboard4 = InlineKeyboardMarkup()
inlinekeyboard4.add(InlineKeyboardButton(text="◀️ Kategoriyalar", callback_data="categories"),
InlineKeyboardButton(text="🏠 Menyu", callback_data="back"))

inlinekeyboard5 = InlineKeyboardMarkup()
inlinekeyboard5.add(InlineKeyboardButton(text="◀️ Kategoriyalar", callback_data="categories"),
InlineKeyboardButton(text="🏠 Menyu", callback_data="back"))

inlinekeyboard6 = InlineKeyboardMarkup()
inlinekeyboard6.add(InlineKeyboardButton(text="◀️ Kategoriyalar", callback_data="categories"),
InlineKeyboardButton(text="🏠 Menyu", callback_data="back"))

inlinekeyboard7 = InlineKeyboardMarkup()
inlinekeyboard7.add(InlineKeyboardButton(text="◀️ Kategoriyalar", callback_data="categories"),
InlineKeyboardButton(text="🏠 Menyu", callback_data="back"))

inlinekeyboard8 = InlineKeyboardMarkup()
inlinekeyboard8.add(InlineKeyboardButton(text="◀️ Kategoriyalar", callback_data="categories"),
InlineKeyboardButton(text="🏠 Menyu", callback_data="back"))

exit = InlineKeyboardMarkup()
exit.add(InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="back"))

gotohome = InlineKeyboardMarkup()
gotohome.add(InlineKeyboardButton(text="◀️ Orqaga", callback_data="back"))

category = InlineKeyboardMarkup()
category.add(InlineKeyboardButton(text="Filmlar", callback_data="films"),
InlineKeyboardButton(text="Seriallar", callback_data="serials"))
category.add(InlineKeyboardButton(text="Anime filmlar", callback_data="anime_films"),
InlineKeyboardButton(text="Anime seriallar", callback_data="anime_serials"))
category.add(InlineKeyboardButton(text="Multfilmlar", callback_data="cartoon"),
InlineKeyboardButton(text="Multseriallar", callback_data="cartoon_serials"))
category.add(InlineKeyboardButton(text="TV-shou", callback_data="tv"))
category.add(InlineKeyboardButton(text="◀️ Orqaga", callback_data="back"))

contacts = InlineKeyboardMarkup()
contacts.add(InlineKeyboardButton(text="✈️ Bizning kanal", url="https://t.me/kinozzztg"),
InlineKeyboardButton(text="📝 Bizning chat", url="https://t.me/Kinozzz_chat"))
contacts.add(InlineKeyboardButton(text="◀️ Orqaga", callback_data="back"))

about = InlineKeyboardMarkup()
# about.add(InlineKeyboardButton(text="🖊️ Вопросы / Ответы", callback_data="faq"))
about.add(InlineKeyboardButton(text="◀️ Назад", callback_data="back"))

search = InlineKeyboardMarkup()
search.add(InlineKeyboardButton(text="🆔 KinoPoisk ID bo‘yicha", callback_data="search_id"))
search.add(InlineKeyboardButton(text="🖊️ Nomi bo‘yicha", callback_data="categories"))
search.add(InlineKeyboardButton(text="◀️ Orqaga", callback_data="back"))

go_poisk = InlineKeyboardMarkup()
# about.add(InlineKeyboardButton(text="🖊️ Вопросы / Ответы", callback_data="faq"))
go_poisk.add(InlineKeyboardButton(text="◀️ Orqaga", callback_data="poisk"))


# БОЛЬШЕ ТГ БОТОВ НА CONFF.ORG
# Наш telegram канал @tg_inc_softw