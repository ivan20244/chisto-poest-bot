import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

SYSTEM_PROMPT = "Ты контент-агент для бренда Чисто поесть. Помогаешь вести TikTok, Telegram и Instagram об еде. Язык: русский. Стиль: дружелюбный."

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Получено сообщение: {update.message.text}")
    try:
        response = model.generate_content(SYSTEM_PROMPT + "\n\n" + update.message.text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await update.message.reply_text("Ошибка, попробуй ещё раз.")

app = ApplicationBuilder().token(os.environ["TELEGRAM_TOKEN"]).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling(drop_pending_updates=True)
