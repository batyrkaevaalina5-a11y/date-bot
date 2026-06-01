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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Получена команда /start от {update.effective_user.id}")
    keyboard = [[InlineKeyboardButton("💫 Выбрать свидание", web_app=WebAppInfo(url=APP_URL))]]
    await update.message.reply_text(
        "Привет! 🥰\nВыбери идею свидания — она сразу узнает!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Получено сообщение: {update.message.text}")
    await update.message.reply_text("Нажми кнопку ниже чтобы выбрать свидание!")

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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    logger.info("Бот запущен!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
