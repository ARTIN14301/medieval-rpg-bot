# main.py
# ============================================
# هسته اصلی بات - نقطه ورود
# ============================================

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

from config import Config
from database.db import init_database, get_session
from database.schema import User

# ===== اضافه کردن هندلر ثبت‌نام =====
from handlers.register import register_start, handle_name_input, class_callback, cancel_register

# ============================================
# تنظیمات لاگینگ
# ============================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================
# کامند start
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """کامند start - خوش‌آمدگویی"""
    await update.message.reply_text(
        "⚔️ **به دنیای Medieval خوش آمدی!** ⚔️\n\n"
        "یک دنیای فانتزی قرون وسطایی منتظر توست.\n\n"
        "📋 **برای شروع:**\n"
        "• `/register` - ثبت‌نام در بازی\n"
        "• `/profile` - مشاهده پروفایل\n\n"
        "🔥 **آماده‌ای که به یک افسانه تبدیل شی؟**"
    )

# ============================================
# کامندهای فارسی (بدون /)
# ============================================

async def handle_farsi_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش کامندهای فارسی (بدون اسلش)"""
    text = update.message.text.strip()
    
    if text == "شروع":
        await start(update, context)
    elif text == "ثبت‌نام":
        await register_start(update, context)
    elif text == "لغو":
        await cancel_register(update, context)
    else:
        # اگه هیچکدوم نبود، نادیده بگیر
        pass

# ============================================
# اجرا
# ============================================

def main():
    """نقطه ورود اصلی"""
    
    # راه‌اندازی دیتابیس
    init_database()
    logger.info("✅ دیتابیس آماده شد")
    
    # ساخت اپلیکیشن
    app = Application.builder().token(Config.BOT_TOKEN).build()
    
    # ===== کامندهای انگلیسی (با /) =====
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register_start))
    app.add_handler(CommandHandler("cancel", cancel_register))
    
    # ===== کالبک‌ها (دکمه‌ها) =====
    app.add_handler(CallbackQueryHandler(class_callback, pattern="^class_"))
    
    # ===== هندلر اسم (برای دریافت اسم در ثبت‌نام) =====
    # این هندلر فقط وقتی کار می‌کنه که کاربر توی حالت waiting_for_name باشه
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name_input),
        group=1
    )
    
    # ===== کامندهای فارسی (بدون /) =====
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_farsi_commands),
        group=2
    )
    
    # ===== اجرا =====
    logger.info("🚀 بات روشن شد!")
    app.run_polling()

if __name__ == "__main__":
    main()
