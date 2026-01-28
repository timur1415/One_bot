import logging
import re
from start import start
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
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from config.states import AMOUNT, TO_CURRENCY, TO_CURRENCY_SELECTED

from forex_python.converter import CurrencyRates

tr = CurrencyRates()

def extract_currency_code(text):
    match = re.search(r'([A-Z]{3})', text)
    return match.group(1) if match else None


async def convert_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        ["🇺�USD🇺🇸", "🇪🇺EUR🇪🇺"],
        ["🇬🇧GBP🇬🇧", "🇯🇵JPY🇯🇵"],
        ["🇨🇳CNY🇨🇳", "🇹🇷TRY🇹🇷"],
        ["🇮🇳INR🇮🇳", "🇦🇺AUD🇦🇺"],
        ["🇧🇷BRL🇧🇷", "🇨🇦CAD🇨🇦"],
        ["🇨🇭CHF🇨🇭", "🇨🇿CZK🇨🇿"],
        ["🇩🇰DKK🇩🇰", "🇭🇰HKD🇭🇰"],
        ["🇭🇺HUF🇭🇺", "🇮🇩IDR🇮🇩"],
        ["🇮🇱ILS🇮🇱", "🇮🇸ISK🇮🇸"],
        ["🇰🇷KRW🇰🇷", "🇲🇽MXN🇲🇽"],
        ["🇲🇾MYR🇲🇾", "🇳🇴NOK🇳🇴"],
        ["🇳🇿NZD🇳🇿", "🇵🇭PHP🇵🇭"],
        ["🇵🇱PLN🇵🇱", "🇷🇴RON🇷🇴"],
        ["🇸🇪SEK🇸🇪", "🇸🇬SGD🇸🇬"],
        ["🇹🇭THB🇹🇭", "🇿🇦ZAR🇿🇦"],
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выберите валюту, из которой хотите конвертировать:",
        reply_markup=markup,
    )

    return TO_CURRENCY


async def to_currency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["from_currency"] = extract_currency_code(update.effective_message.text)
    keyboard = [
        ["🇺�USD🇺🇸", "🇪🇺EUR🇪🇺"],
        ["🇬🇧GBP🇬🇧", "🇯🇵JPY🇯🇵"],
        ["🇨🇳CNY🇨🇳", "🇹🇷TRY🇹🇷"],
        ["🇮🇳INR🇮🇳", "🇦🇺AUD🇦🇺"],
        ["🇧🇷BRL🇧🇷", "🇨🇦CAD🇨🇦"],
        ["🇨🇭CHF🇨🇭", "🇨🇿CZK🇨🇿"],
        ["🇩🇰DKK🇩🇰", "🇭🇰HKD🇭🇰"],
        ["🇭🇺HUF🇭🇺", "🇮🇩IDR🇮🇩"],
        ["🇮🇱ILS🇮🇱", "🇮🇸ISK🇮🇸"],
        ["🇰🇷KRW🇰🇷", "🇲🇽MXN🇲🇽"],
        ["🇲🇾MYR🇲🇾", "🇳🇴NOK🇳🇴"],
        ["🇳🇿NZD🇳🇿", "🇵🇭PHP🇵🇭"],
        ["🇵🇱PLN🇵🇱", "🇷🇴RON🇷🇴"],
        ["🇸🇪SEK🇸🇪", "🇸🇬SGD🇸🇬"],
        ["🇹🇭THB🇹🇭", "🇿🇦ZAR🇿🇦"],
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Вы выбрали {context.user_data['from_currency']}, теперь выберите валюту, в которую хотите конвертировать:",
        reply_markup=markup,
    )

    return TO_CURRENCY_SELECTED 

async def to_currency_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["to_currency"] = extract_currency_code(update.effective_message.text)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Введите сумму для конвертации из {context.user_data['from_currency']} в {context.user_data['to_currency']}:",
    )
    return AMOUNT

async def amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("выход", callback_data="start")]]
    markup = InlineKeyboardMarkup(keyboard)
    try:
        amount_value = float(update.effective_message.text)
        to_currency = context.user_data["to_currency"]
        from_currency = context.user_data["from_currency"]

        result = tr.convert(from_currency, to_currency, amount_value)
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{amount_value} {from_currency} = {result:.2f} {to_currency}",
            reply_markup=markup,
        )
        
        
    except ValueError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Пожалуйста, введите корректную сумму.",
        )
        return AMOUNT
    except Exception as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Ошибка при конвертации валют. Пожалуйста, повторите попытку позже.",
            reply_markup=markup,
        )
        logging.error(f"Converter error: {str(e)}")
        return AMOUNT
