import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from config import Config
from database.db import init_database
from handlers.register import register_start, handle_name_input, class_callback
from utils.messages import get_start_message


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_start_message())

async def farsi_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text == "شروع":
        await start(update, context)
    elif text == "ثبت‌نام":
        await register_start(update, context)

def main():
    init_database()
    logger.info("✅ دیتابیس آماده شد")
    
    app = Application.builder().token(Config.BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register_start))
    app.add_handler(CallbackQueryHandler(class_callback, pattern="^class_"))
    
    # هندلر دریافت اسم با اولویت بالا
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name_input),
        group=1
    )
    
    # هندلر کامندهای فارسی
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, farsi_handler),
        group=2
    )
    
    logger.info("🚀 بات روشن شد!")
    app.run_polling()

if __name__ == "__main__":
    main()
