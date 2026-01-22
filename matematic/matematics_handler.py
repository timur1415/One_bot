from telegram.ext import (
    ContextTypes,
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from config.states import EQUATION_MENU, MATEMATICS_MENU


async def matematics_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("калькулятор", callback_data="calculator")],
        [InlineKeyboardButton("решение уравнений", callback_data="equation")],
        [InlineKeyboardButton("в главное меню", callback_data="go_main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Выберите раздел математики:", reply_markup=reply_markup
    )
    return MATEMATICS_MENU


async def equation_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("фото уравнения", callback_data="photo_equation")],
        [InlineKeyboardButton("текст уравнение", callback_data="input_equation")],
        [InlineKeyboardButton("в главное меню", callback_data="go_main_menu")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Выберите способ ввода уравнения:", reply_markup=markup
    )
    return EQUATION_MENU
