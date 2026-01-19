from telegram.ext import ContextTypes
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from config.states import FIRST_NUMBER, LAST_NUMBER, OPERATION


async def first_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Введите первое число:"
    )
    return FIRST_NUMBER

async def get_first_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard_operation = [['+', '-'], ['*', '/']]
    markup_operation = ReplyKeyboardMarkup(keyboard_operation)
    keyboard_false = [[InlineKeyboardButton("начать заново", callback_data="cancel")]]
    markup_false = InlineKeyboardMarkup(keyboard_false)
    try:
        first_num = float(update.message.text)
        context.user_data['first_number'] = first_num
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Выберете знак операции:",
            reply_markup=markup_operation
        )
        return OPERATION
    except ValueError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Пожалуйста, введите корректное число.", reply_markup=markup_false
        )

async def get_operation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    operation = update.message.text
    context.user_data['operation'] = operation
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Введите второе число:", reply_markup=ReplyKeyboardRemove()
    )
    return LAST_NUMBER

async def get_last_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("начать заново", callback_data="cancel")]]
    markup = InlineKeyboardMarkup(keyboard)
    try:
        last_num = float(update.message.text)
        context.user_data['last_number'] = last_num

        first_num = context.user_data['first_number']
        operation = context.user_data['operation']

        if operation == '+':
            result = first_num + last_num
        elif operation == '-':
            result = first_num - last_num
        elif operation == '*':
            result = first_num * last_num
        elif operation == '/':
            if last_num == 0:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, text="Ошибка: Деление на ноль невозможно.",
                    reply_markup=markup
                )
        
            result = first_num / last_num
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text="Ошибка: Некорректная операция.",
                reply_markup=markup
            )
    

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Результат:\n{first_num} {operation} {last_num} = {result}",
            reply_markup=markup
        )

    except ValueError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Пожалуйста, введите корректное число.",
            reply_markup=markup
        )
