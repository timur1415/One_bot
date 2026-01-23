from telegram.ext import (
    ContextTypes,
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from openai import AsyncOpenAI

from config.states import EQUATION_TEXT_RESULT

from config.config import CHAT_GPT_TOKEN
from start import start


async def equation_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Пожалуйста, введите уравнение в текстовом формате:",
    )
    return EQUATION_TEXT_RESULT


async def equation_text_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    equation = update.effective_message.text

    client = AsyncOpenAI(api_key=CHAT_GPT_TOKEN)

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Ты профессиональный математик. Решай уравнения пошагово в столбик. Используй только цифры, знаки операций (+, -, *, /), = и переносы строк. БЕЗ НИКАКИХ букв, текста и объяснений. Каждый шаг на новой строке.",
            },
            {
                "role": "user",
                "content": f"Реши уравнение пошагово в столбик:\n{equation}",
            },
        ],
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response.choices[0].message.content,
    )
    return await start(update, context)