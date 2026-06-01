import os
import json
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ─── НАСТРОЙКИ (берутся из переменных окружения Railway) ───
TOKEN   = os.environ.get("BOT_TOKEN")   # токен от @BotFather
YOUR_ID = int(os.environ.get("YOUR_ID"))  # твой Telegram ID из @userinfobot
APP_URL = os.environ.get("APP_URL")     # ссылка на сайт с Netlify, например https://my-dates.netlify.app

# ─── /start — главное меню ───
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(
            text="💫 Выбрать свидание",
            web_app=WebAppInfo(url=APP_URL)
        )
    ]]
    await update.message.reply_text(
        "Привет! 🥰\n\nНажми кнопку ниже, выбери идею свидания — и она сразу получит уведомление!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ─── Получаем данные из Mini App (когда парень нажал «Отправить ей») ───
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = json.loads(update.message.web_app_data.data)
        emoji = data.get("emoji", "💌")
        title = data.get("title", "")
        desc  = data.get("desc", "")

        # Сообщение парню — подтверждение
        await update.message.reply_text(
            f"Отлично! Она уже знает о твоём выборе 🥰\n\n{emoji} {title}"
        )

        # Уведомление тебе
        await context.bot.send_message(
            chat_id=YOUR_ID,
            text=(
                f"💌 Он выбрал свидание!\n\n"
                f"{emoji} *{title}*\n\n"
                f"{desc}"
            ),
            parse_mode="Markdown"
        )

    except Exception as e:
        print(f"Ошибка обработки данных: {e}")
        await update.message.reply_text("Что-то пошло не так, попробуй ещё раз 🌙")

# ─── ЗАПУСК ───
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    print("Бот запущен ✓")
    app.run_polling()

if __name__ == "__main__":
    main()
