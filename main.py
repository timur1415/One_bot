import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler,
    PicklePersistence,
)
from config.config import TOKEN

from config.states import TONE, TRANSLATION, ANSWER, MAIN_MENU,  LANG_TO #LANG_FROM,

from translation.translation import translation_handler, tone_handler, answer_handler, lang_to_handler#lang_from_handler, 

from start import start

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

if __name__ == "__main__":
    persistence = PicklePersistence(filepath="game_bot")
    application = ApplicationBuilder().token(TOKEN).persistence(persistence).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(translation_handler, pattern='^start_translation$')
            ],
            TONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, tone_handler)
            ],
            TRANSLATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, translation_handler)
            ],
            ANSWER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, answer_handler),
                CallbackQueryHandler(start, pattern='^go_main_menu$')
            ],
            # LANG_FROM: [
            #     MessageHandler(filters.TEXT & ~filters.COMMAND, lang_from_handler)
            # ],
            LANG_TO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, lang_to_handler)
            ],
        },                      
        fallbacks=[CommandHandler("start", start)],
        name="OneBot",
        persistent=True
    )

    application.add_handler(conv_handler)

    application.run_polling()