from openai import AsyncOpenAI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config.config import CHAT_GPT_TOKEN
from config.states import AI


client = AsyncOpenAI(api_key=CHAT_GPT_TOKEN)

async def ai_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("в главное меню", callback_data="go_main_menu")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    user_message = update.effective_message.text

    # Если истории нет — создаём её
    if "history" not in context.user_data:
        context.user_data["history"] = [
            {
                "role": "system",
                "content": "отвечай на выставленные вопросы максимально кратко и по существу без лишних слов, не используй вводные слова и фразы, не пиши ничего лишнего, только ответ на поставленный вопрос",
            }
        ]

    # Добавляем сообщение пользователя
    context.user_data["history"].append({
        "role": "user",
        "content": user_message
    })

    # Отправляем всю историю в модель
    response = await client.chat.completions.create(
        model="gpt-5.2",
        messages=context.user_data["history"],
    )

    assistant_reply = response.choices[0].message.content

    # Сохраняем ответ ассистента в историю
    context.user_data["history"].append({
        "role": "assistant",
        "content": assistant_reply
    })

    # Ограничение истории (например, последние 10 сообщений)
    context.user_data["history"] = context.user_data["history"][-5:]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=assistant_reply, reply_markup=markup
    )
    return AI