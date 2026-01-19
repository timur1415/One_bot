import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler,
    PicklePersistence,
    ContextTypes,
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from config.states import MAIN_MENU

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("перевод текста в нужном тоне ", callback_data='start_translation')],
                [InlineKeyboardButton("математика", callback_data='start_mathematics')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    if query:
        await query.answer()
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="чем ещё могу помочь?",
            reply_markup=reply_markup
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Добро пожаловать! Чем я могу помочь?",
            reply_markup=reply_markup
        )
    return MAIN_MENU