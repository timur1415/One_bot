from telegram.ext import (
    ContextTypes,
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from openai import AsyncOpenAI

from config.config import CHAT_GPT_TOKEN

from config.states import EQUATION_PHOTO_RESULT

async def equation_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query   
    await query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Пожалуйста, отправьте фотографию с уравнением:",
    )
    return EQUATION_PHOTO_RESULT

async def equation_photo_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton('в главное меню', callback_data='go_main_menu')]]
    markup = InlineKeyboardMarkup(keyboard)
    photo_file = await update.message.photo[-1].get_file()
    photo_path = await photo_file.download_to_drive()

    client = AsyncOpenAI(api_key=CHAT_GPT_TOKEN)
    