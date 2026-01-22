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

from config.states import (
    TONE,
    TRANSLATION,
    ANSWER,
    MAIN_MENU,
    LANG_TO,
    MATEMATICS_MENU,
    FIRST_NUMBER,
    LAST_NUMBER,
    OPERATION,
    EQUATION_MENU,
    EQUATION_TEXT_RESULT,
    EQUATION_PHOTO_RESULT,
)

from matematic.equation.equation_text import equation_text_handler
from translation.translation import (
    translation_handler,
    tone_handler,
    answer_handler,
    lang_to_handler,
) 

from start import start

from matematic.matematics_handler import matematics_handler, equation_handler

from matematic.calculator import (
    first_number,
    get_first_number,
    get_operation,
    get_last_number,
)

from matematic.equation.equation_text import equation_text_result

from matematic.equation.equation_photo import equation_photo_handler, equation_photo_result

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

if __name__ == "__main__":
    persistence = PicklePersistence(filepath="one_bot")
    application = ApplicationBuilder().token(TOKEN).persistence(persistence).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(
                    translation_handler, pattern="^start_translation$"
                ),
                CallbackQueryHandler(matematics_handler, pattern="^start_mathematics$"),
            ],
            MATEMATICS_MENU: [
                CallbackQueryHandler(first_number, pattern="^calculator$"),
                CallbackQueryHandler(
                    equation_handler, pattern="^equation$"
                ),
            ],
            FIRST_NUMBER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_first_number),
                CallbackQueryHandler(start, pattern="^cancel$"),
            ],
            OPERATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_operation)],
            LAST_NUMBER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_last_number),
                CallbackQueryHandler(start, pattern="^cancel$"),
            ],
            TONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, tone_handler)],
            TRANSLATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, translation_handler)
            ],
            ANSWER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, answer_handler),
                CallbackQueryHandler(start, pattern="^go_main_menu$"),
            ],
            LANG_TO: [MessageHandler(filters.TEXT & ~filters.COMMAND, lang_to_handler)],
            EQUATION_MENU: [
                CallbackQueryHandler(equation_photo_handler, pattern="^photo_equation$"),
                CallbackQueryHandler(equation_text_handler, pattern="^input_equation$"),
                CallbackQueryHandler(start, pattern="^go_main_menu$"),
            ],
            EQUATION_TEXT_RESULT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, equation_text_result),
                CallbackQueryHandler(start, pattern="^go_main_menu$"),
            ],
            EQUATION_PHOTO_RESULT: [
                MessageHandler(filters.PHOTO & ~filters.COMMAND, equation_photo_result),
                CallbackQueryHandler(start, pattern="^go_main_menu$"),
            ]
        },
        fallbacks=[CommandHandler("start", start)],
        name="OneBot",
        persistent=True,
    )

    application.add_handler(conv_handler)

    application.run_polling()
