from telegram.ext import (
    ContextTypes)

from telegram import Update

from start import start
from config.states import CORRECTION

from openai import OpenAI
from config.config import CHAT_GPT_TOKEN

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Введите текст для исправления ошибок:"
    )
    return CORRECTION

async def correction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.effective_message.text
    client = OpenAI(api_key=CHAT_GPT_TOKEN)
    response = client.chat.completions.create(
        model="gpt-5.2",
        messages=[
            {
                "role": "system",
                "content": f"Ты - помощник, который исправляет ошибки в тексте. Исправь ошибки в следующем тексте: {user_text}"
            },
            {
                "role": "user",
                "content": f'Исправь ошибки в следующем тексте: {user_text}'
            }
        ]
    )
    corrected_text = response.choices[0].message.content
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Исправленный текст:\n\n{corrected_text}"
    )
    return await start(update, context)