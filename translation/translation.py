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

from config.states import TONE, ANSWER, MAIN_MENU, LANG_TO

from config.config import CHAT_GPT_TOKEN

from openai import AsyncOpenAI

from start import start


async def translation_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="что нужно переводить?"
    )
    return TONE


async def tone_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["translation"] = update.effective_message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="в какой тон?"
    )
    return LANG_TO


async def lang_to_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["tone"] = update.effective_message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="на какой язык переводить?"
    )
    return ANSWER


async def answer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("в главное меню", callback_data="go_main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    translation = context.user_data["translation"]
    tone = context.user_data["tone"]
    lang_to = update.effective_message.text

    client = AsyncOpenAI(api_key=CHAT_GPT_TOKEN)

    response = await client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": "Ты профессиональный переводчик с руского на английский. Ты должен переводить тексты в заданном тоне максимально точно и естественно.",
            },
            {
                "role": "assistant",
                "content": f"Распознай язык на котором тебе пишут и переведи его на {lang_to} язык в заданном тоне: {translation} Тон: {tone}. Ответь только переводом.",
            },
            {"role": "user", "content": f"{translation}"},
        ],
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response.output_text,
        reply_markup=reply_markup,
    )