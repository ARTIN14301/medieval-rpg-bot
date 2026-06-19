import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from config import Config
from database.db import init_database
from handlers.register import register_start, handle_name_input, class_callback
from utils.messages import get_start_message
from handlers.army import chosearmy, army_callback, leavearmy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_start_message())

async def handle_farsi_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش کامندهای فارسی (بدون اسلش)"""
    text = update.message.text.strip()
    
    if text == "شروع":
        await start(update, context)
    elif text == "ثبت‌نام":
        await register_start(update, context)
    elif text == "لغو":
        await cancel_register(update, context)
    # ===== کامندهای جدید ارتش =====
    elif text == "ارتش":
        await chosearmy(update, context)
    elif text == "خروج":
        await leavearmy(update, context)
    # و بقیه کامندها...

def main():
    init_database()
    logger.info("✅ دیتابیس آماده شد")
    
    app = Application.builder().token(Config.BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register_start))
    app.add_handler(CallbackQueryHandler(class_callback, pattern="^class_"))
    # ===== کامندهای ارتش =====
    app.add_handler(CommandHandler("chosearmy", chosearmy))
    app.add_handler(CommandHandler("leavearmy", leavearmy))

# ===== کالبک ارتش =====
    app.add_handler(CallbackQueryHandler(army_callback, pattern="^army_"))
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
