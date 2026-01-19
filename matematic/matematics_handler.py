from telegram.ext import (
    ContextTypes,
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from config.states import MATEMATICS_MENU


async def matematics_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("калькулятор", callback_data="calculator")],
        [InlineKeyboardButton("решение уравнений", callback_data="equation_solver")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Выберите раздел математики:", reply_markup=reply_markup
    )
    return MATEMATICS_MENU
