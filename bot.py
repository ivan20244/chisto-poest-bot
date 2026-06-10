import os
import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

SYSTEM_PROMPT = """Ты контент-агент для бренда Чисто поесть. Помогаешь вести TikTok, Telegram и Instagram об еде. Аудитория: все кто любит вкусно поесть. Стиль: дружелюбный, с лёгким юмором. Язык: русский."""

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = model.generate_content(SYSTEM_PROMPT + "\n\nПользователь: " + user_message)
    await update.message.reply_text(response.text)

def main():
    app = Application.builder().token(os.environ["TELEGRAM_TOKEN"]).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if name == "main":
    main()
