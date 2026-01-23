from telegram.ext import (
    ContextTypes,
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from openai import AsyncOpenAI
import base64
import os

from config.config import CHAT_GPT_TOKEN

from config.states import EQUATION_PHOTO_RESULT

from start import start

async def equation_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query   
    await query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Пожалуйста, отправьте фотографию с уравнением:",
    )
    return EQUATION_PHOTO_RESULT

async def equation_photo_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    photo_path = await photo_file.download_to_drive()

    with open(photo_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    client = AsyncOpenAI(api_key=CHAT_GPT_TOKEN)

    response = await client.chat.completions.create(
        model="gpt-5.2",
        # reasoning=''
        messages=[
            {
                "role": "system",
                "content": """Ты профессиональный математик. Твоя задача решить уравнение, которое показано на фотографии.

ПРАВИЛА:
1. Решай пошагово в столбик
2. Если это квадратное уравнение - используй дискриминант и выпиши формулу
3. Используй ТОЛЬКО: цифры, знаки операций (+, -, *, /, ^), знак равенства (=), скобки ()
4. ЗАПРЕЩЕНО: буквы, текст, слова, объяснения, комментарии
5. Каждый шаг решения - на новой строке
6. если идёт умножение числа на x - пиши это как 2x, 3x и т.д., без знака умножения

Пример формата ответа:
2x + 5 = 13
2x = 13 - 5
2x = 8
x = 8 / 2
x = 4""",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Реши уравнение пошагово в столбик на этой фотографии:"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ],
            }
        ]
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response.choices[0].message.content,
    )
    
    
    try:
        os.remove(photo_path)
    except Exception as e:
        print(f"Ошибка при удалении файла: {e}")

    return await start(update, context)    