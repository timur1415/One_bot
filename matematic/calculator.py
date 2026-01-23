from telegram.ext import ContextTypes
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from config.states import FIRST_NUMBER, LAST_NUMBER, OPERATION
from start import start


async def first_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Введите первое число:"
    )
    return FIRST_NUMBER


async def get_first_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard_operation = [["+", "-"], ["*", "/"]]
    markup_operation = ReplyKeyboardMarkup(keyboard_operation)
    try:
        first_num = float(update.message.text)
        context.user_data["first_number"] = first_num
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Выберете знак операции:",
            reply_markup=markup_operation,
        )
        return OPERATION
    except ValueError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Пожалуйста, введите корректное число.",
        )
        return await first_number(update, context)


async def get_operation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    operation = update.message.text
    context.user_data["operation"] = operation
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Введите второе число:",
        reply_markup=ReplyKeyboardRemove(),
    )
    return LAST_NUMBER


async def get_last_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        last_num = float(update.message.text)
        context.user_data["last_number"] = last_num

        first_num = context.user_data["first_number"]
        operation = context.user_data["operation"]

        if operation == "+":
            result = first_num + last_num
        elif operation == "-":
            result = first_num - last_num
        elif operation == "*":
            result = first_num * last_num
        elif operation == "/":
            result = first_num / last_num
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Ошибка: Некорректная операция.",
            )
            return await first_number(update, context)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Результат:\n{first_num} {operation} {last_num} = {result}",
        )
        return await start(update, context)

    except ValueError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Пожалуйста, введите корректное число.",
        )
        return await first_number(update, context)
