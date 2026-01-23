from telegram.ext import (
    ContextTypes,
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from config.states import GAME_HANDLER


async def game_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("камень ножницы бумага", callback_data="start_knb")],
        [InlineKeyboardButton("в главное меню", callback_data="go_main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Выберите игру:", reply_markup=reply_markup
    )
    return GAME_HANDLER