from telegram.ext import (
    ContextTypes,
)

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from config.states import TEXT_MENU


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(
                "исправление ошибок в тексте", callback_data="correction"
            )
        ],
        [InlineKeyboardButton("выход в главное меню", callback_data="go_main_menu")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Выберите действие с текстом:", reply_markup=markup
    )
    return TEXT_MENU
