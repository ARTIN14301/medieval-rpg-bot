# main.py
# ============================================
# هسته اصلی بات - نقطه ورود
# ============================================

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

from config import Config
from database.db import init_database
from handlers.register import register_start, handle_name_input, class_callback, cancel_register
from handlers.army import chosearmy, army_callback, leavearmy
from utils.messages import get_start_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def reply(update: Update, text: str):
    """ارسال پیام با MarkdownV2"""
    await update.message.reply_text(text, parse_mode="MarkdownV2")

async def reply_callback(query, text: str):
    """ویرایش پیام با MarkdownV2"""
    await query.edit_message_text(text, parse_mode="MarkdownV2")

# ============================================
# کامند start
# ============================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await reply(update, get_start_message())

# ============================================
# کامندهای فارسی (بدون /)
# ============================================
async def farsi_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if text == "شروع":
        await start(update, context)
    elif text == "ثبت‌نام":
        await register_start(update, context)
    elif text == "لغو":
        await cancel_register(update, context)
    elif text == "ارتش":
        await chosearmy(update, context)
    elif text == "خروج":
        await leavearmy(update, context)

# ============================================
# اجرا
# ============================================
def main():
    init_database()
    logger.info("✅ دیتابیس آماده شد")
    
    app = Application.builder().token(Config.BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register_start))
    app.add_handler(CommandHandler("cancel", cancel_register))
    app.add_handler(CommandHandler("chosearmy", chosearmy))
    app.add_handler(CommandHandler("leavearmy", leavearmy))
    
    app.add_handler(CallbackQueryHandler(class_callback, pattern="^class_"))
    app.add_handler(CallbackQueryHandler(army_callback, pattern="^army_"))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name_input), group=1)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, farsi_handler), group=2)
    
    logger.info("🚀 بات روشن شد!")
    app.run_polling()

if __name__ == "__main__":
    main()
