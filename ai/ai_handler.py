from telegram.ext import (
    ContextTypes,
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from config.states import AI_MENU


async def ai_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("отвветы на вопросы (ии)", callback_data="ai_answer")],
        [InlineKeyboardButton("в главное меню", callback_data="go_main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="", reply_markup=reply_markup
    )
    return AI_MENU