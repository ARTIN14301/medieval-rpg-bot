# main.py
# ============================================
# هسته اصلی بات - نقطه ورود
# ============================================

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from config import Config
from database.db import init_database, get_session
from database.schema import User

# ============================================
# تنظیمات لاگینگ
# ============================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============================================
# دکوریتور بررسی ثبت‌نام
# ============================================

def require_registered(func):
    """دکوریتور برای چک کردن ثبت‌نام کاربر"""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = str(update.effective_user.id)
        session = get_session()
        user = session.query(User).filter_by(telegram_id=user_id).first()
        session.close()
        
        if not user:
            await update.message.reply_text(
                "❌ اول باید با /register ثبت‌نام کنی!"
            )
            return
        
        return await func(update, context, user, *args, **kwargs)
    return wrapper

# ============================================
# کامندها
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """کامند start - خوش‌آمدگویی"""
    await update.message.reply_text(
        "⚔️ **به دنیای Medieval خوش آمدی!** ⚔️\n\n"
        "یک دنیای فانتزی قرون وسطایی منتظر توست.\n\n"
        "📋 **برای شروع:**\n"
        "• `/register` - ثبت‌نام در بازی\n"
        "• `/profile` - مشاهده پروفایل\n"
        "• `/help` - راهنمای کامل\n\n"
        "🔥 **آماده‌ای که به یک افسانه تبدیل شی؟**"
    )

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """کامند register - ثبت‌نام کاربر"""
    # فعلاً ساده - بعداً کامل می‌شه
    await update.message.reply_text(
        "📝 **مرحله ۱: انتخاب اسم**\n\n"
        "یک اسم برای شخصیتت انتخاب کن:\n"
        "• حداکثر ۱۵ حرف\n"
        "• فقط حروف انگلیسی و اعداد و _\n\n"
        "مثال: `ArashTheGreat`"
    )

# ============================================
# هندلرهای فارسی (بدون /)
# ============================================

async def handle_farsi_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش کامندهای فارسی (بدون اسلش)"""
    text = update.message.text.strip()
    
    if text == "شروع":
        await start(update, context)
    elif text == "ثبت‌نام":
        await register(update, context)
    # و بقیه کامندها...

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
    app.add_handler(CommandHandler("register", register))
    # بقیه کامندها اضافه می‌شن...
    
    # ===== کامندهای فارسی (بدون /) =====
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_farsi_commands
    ))
    
    # ===== اجرا =====
    logger.info("🚀 بات روشن شد!")
    app.run_polling()

if __name__ == "__main__":
    main()
