
import os
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
TOKEN   = os.environ.get("BOT_TOKEN")
YOUR_ID = int(os.environ.get("YOUR_ID"))
APP_URL = os.environ.get("APP_URL")
 
IDEAS = {
    "1":  ("🕯️", "Ужин при свечах дома",        "Накрой красивый стол, зажги свечи и приготовь её любимое блюдо."),
    "2":  ("🌅", "Встретить рассвет вместе",     "Уедьте заранее и встретьте рассвет с кофе в руках. Незабываемо."),
    "3":  ("💌", "Письма друг другу",            "Каждый пишет письмо о том, что любит в партнёре. Потом читаете вслух."),
    "4":  ("🚴", "Велопрогулка по городу",       "Возьмите велосипеды и исследуйте незнакомые улочки вместе."),
    "5":  ("⛸️", "Каток + горячий шоколад",      "После катка обязательно греться горячим шоколадом."),
    "6":  ("🏔️", "Пешеходный поход",             "Красивый маршрут + пикник с собой. Природа и движение — лучшая пара."),
    "7":  ("🎬", "Киномарафон с темой",          "Выбери тему: режиссёр или жанр. Попкорн, плед, уют."),
    "8":  ("🍕", "Готовим вместе",               "Сложный рецепт, который никогда не пробовали."),
    "9":  ("🎮", "Игровой вечер",                "Настолки или видеоигры. Добавьте «ставки» — становится веселее."),
    "10": ("🗺️", "Мини-путешествие",             "Электричка без цели, случайная станция. Исследуйте что найдёте."),
    "11": ("📸", "Фотопрогулка",                 "Фотозадания друг другу: «найди что-то синее», «старейшее здание»."),
    "12": ("🎭", "Квест или escape room",        "Решайте загадки вместе — командная работа и много смеха."),
    "13": ("🍜", "Ресторан новой кухни",         "Кухня, которую никогда не пробовали: эфиопская, грузинская, вьетнамская."),
    "14": ("🍷", "Дегустация дома",              "Несколько вин или сыров разных видов — домашняя дегустация."),
    "15": ("☕", "Кофейный тур по городу",       "3–4 кофейни за день, пробуя фирменные напитки в каждой."),
    "16": ("🫧", "Массаж с маслами 1 час",       "Ароматные масла, свечи, приятная музыка. Только вы двое."),
    "17": ("🛁", "Ванна с пеной и вином",        "Свечи, пена, бокал вина — полный релакс и уют."),
    "18": ("🌿", "СПА-вечер дома",               "Маски, пилинги, массаж ног — смешно и расслабляюще одновременно."),
}
 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Получена команда /start от {update.effective_user.id}")
    keyboard = [[InlineKeyboardButton("💫 Выбрать свидание", web_app=WebAppInfo(url=APP_URL))]]
    await update.message.reply_text(
        "Привет! 🥰\nВыбери идею свидания — она сразу узнает!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
 
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    logger.info(f"Получено сообщение: {text} от {update.effective_user.id}")
 
    if text.startswith("CHOICE:"):
        idea_id = text.replace("CHOICE:", "").strip()
        idea = IDEAS.get(idea_id)
        if idea:
            emoji, title, desc = idea
            await update.message.reply_text(f"Отлично! Она уже знает! 🥰\n\n{emoji} {title}")
            await context.bot.send_message(
                chat_id=YOUR_ID,
                text=f"💌 Он выбрал свидание!\n\n{emoji} {title}\n\n{desc}"
            )
            logger.info(f"Уведомление отправлено на ID: {YOUR_ID}")
        return
 
    await update.message.reply_text("Нажми кнопку ниже чтобы выбрать свидание! 💫")
 
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Получены данные из Mini App, отправляю на ID: {YOUR_ID}")
    try:
        data = json.loads(update.message.web_app_data.data)
        emoji = data.get("emoji", "💌")
        title = data.get("title", "")
        desc  = data.get("desc", "")
        await update.message.reply_text(f"Отлично! Она уже знает! 🥰\n\n{emoji} {title}")
        await context.bot.send_message(
            chat_id=YOUR_ID,
            text=f"💌 Он выбрал свидание!\n\n{emoji} {title}\n\n{desc}"
        )
    except Exception as e:
        logger.error(f"Ошибка: {e}")
 
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Бот запущен!")
    app.run_polling(drop_pending_updates=True)
 
if __name__ == "__main__":
    main()
