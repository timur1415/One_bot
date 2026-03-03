from telegram.ext import (
    ContextTypes,
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

from config.states import MAIN_MENU

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("перевод текста в нужном тоне ", callback_data='start_translation')],
                [InlineKeyboardButton("математика", callback_data='start_mathematics')],
                [InlineKeyboardButton("игры", callback_data='start_games')],
                [InlineKeyboardButton("конвертер валют", callback_data='start_converter')],
                [InlineKeyboardButton("работа с текстом", callback_data='text')],
                [InlineKeyboardButton("нейросеть", callback_data='ai')]]
                
    markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    if query:
        await query.answer()
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="чем ещё могу помочь?",
            reply_markup=markup
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Добро пожаловать! Чем я могу помочь?",
            reply_markup=markup
        )
        message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="f",
            reply_markup=ReplyKeyboardRemove(),
        )
        await context.bot.delete_message(
            chat_id=update.effective_chat.id, message_id=message.id
        )
    return MAIN_MENU