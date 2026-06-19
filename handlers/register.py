# handlers/register.py
# ============================================
# سیستم ثبت‌نام کامل با طراحی حرفه‌ای
# ============================================

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database.db import get_session
from database.schema import User
from utils.constants import CLASSES
from utils.messages import (
    get_register_name_message,
    get_register_class_message,
    get_register_success_message,
    get_class_keyboard
)
from config import Config

logger = logging.getLogger(__name__)

# ============================================
# دیکشنری برای ذخیره موقت کاربران در حال ثبت‌نام
# ============================================
waiting_for_name = {}

# ============================================
# ۱. شروع ثبت‌نام
# ============================================

async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    شروع فرآیند ثبت‌نام - مرحله ۱: انتخاب اسم
    """
    user_id = str(update.effective_user.id)
    logger.info(f"🔵 register_start called for user {user_id}")
    
    # چک کردن اینکه کاربر قبلاً ثبت‌نام نکرده
    session = get_session()
    existing = session.query(User).filter_by(telegram_id=user_id).first()
    session.close()
    
    if existing:
        await update.message.reply_text(
            f"❌ شما قبلاً با اسم `{existing.username}` ثبت‌نام کردی!\n"
            f"برای مشاهده پروفایل از `/profile` استفاده کن."
        )
        return
    
    # اضافه کردن کاربر به لیست انتظار
    waiting_for_name[user_id] = True
    
    # ارسال پیام انتخاب اسم با طراحی جدید
    await update.message.reply_text(get_register_name_message())

# ============================================
# ۲. دریافت اسم و ذخیره موقت
# ============================================

async def handle_name_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    دریافت اسم از کاربر و رفتن به مرحله انتخاب کلاس
    """
    user_id = str(update.effective_user.id)
    logger.info(f"🔵 handle_name_input called for user {user_id}")
    
    # چک کردن اینکه کاربر در حالت ثبت‌نام هست
    if user_id not in waiting_for_name:
        logger.info(f"User {user_id} not in waiting_for_name")
        return
    
    name = update.message.text.strip()
    
    # ===== اعتبارسنجی اسم =====
    if len(name) > 15:
        await update.message.reply_text(
            "❌ **اسم خیلی بلند است!**\n"
            "حداکثر ۱۵ حرف مجاز است.\n\n"
            "✏️ لطفاً دوباره تلاش کن:"
        )
        return
    
    if " " in name:
        await update.message.reply_text(
            "❌ **اسم نباید فاصله داشته باشد!**\n"
            "از «_» برای جدا کردن کلمات استفاده کن.\n\n"
            "✏️ لطفاً دوباره تلاش کن:"
        )
        return
    
    if not name.replace("_", "").isalnum():
        await update.message.reply_text(
            "❌ **اسم نامعتبر است!**\n"
            "فقط حروف انگلیسی، اعداد و «_» مجاز است.\n\n"
            "✏️ لطفاً دوباره تلاش کن:"
        )
        return
    
    # ===== چک کردن تکراری نبودن اسم =====
    session = get_session()
    existing = session.query(User).filter_by(username=name).first()
    session.close()
    
    if existing:
        await update.message.reply_text(
            f"❌ **اسم `{name}` قبلاً استفاده شده!**\n"
            "یک اسم دیگر انتخاب کن.\n\n"
            "✏️ لطفاً دوباره تلاش کن:"
        )
        return
    
    # ===== ذخیره اسم در context و رفتن به مرحله بعد =====
    context.user_data['temp_username'] = name
    del waiting_for_name[user_id]
    
    # ارسال پیام انتخاب کلاس با دکمه‌های رنگی
    await update.message.reply_text(
        get_register_class_message(),
        reply_markup=InlineKeyboardMarkup(get_class_keyboard())
    )

# ============================================
# ۳. انتخاب کلاس و ثبت نهایی
# ============================================

async def class_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    پردازش انتخاب کلاس و ذخیره نهایی کاربر در دیتابیس
    """
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    class_key = query.data.replace("class_", "")
    
    logger.info(f"🔵 class_callback called for user {user_id} with class {class_key}")
    
    # ===== چک کردن کلاس معتبر =====
    if class_key not in CLASSES:
        await query.edit_message_text(
            "❌ **کلاس نامعتبر!**\n"
            "لطفاً با `/register` دوباره شروع کن."
        )
        return
    
    # ===== دریافت اسم موقت =====
    temp_username = context.user_data.get('temp_username')
    if not temp_username:
        await query.edit_message_text(
            "❌ **خطا!**\n"
            "لطفاً با `/register` دوباره شروع کن."
        )
        return
    
    # ===== چک کردن دوباره تکراری نبودن اسم (احتمالاً کسی بین مراحل ثبت کرده) =====
    session = get_session()
    existing = session.query(User).filter_by(username=temp_username).first()
    if existing:
        session.close()
        await query.edit_message_text(
            f"❌ **اسم `{temp_username}` بین مراحل ثبت‌نام گرفته شد!**\n"
            "لطفاً با `/register` دوباره شروع کن."
        )
        return
    
    # ===== ایجاد کاربر جدید =====
    try:
        new_user = User(
            telegram_id=user_id,
            username=temp_username,
            class_name=class_key,
            gold=Config.STARTING_GOLD,
            level=1,
            title="کهنه‌سرباز",
            exp=0,
            exp_needed=100,
            wins=0,
            losses=0
        )
        
        session.add(new_user)
        session.commit()
        
        logger.info(f"✅ User {temp_username} registered successfully!")
        
        # ===== پاک کردن داده‌های موقت =====
        context.user_data.pop('temp_username', None)
        session.close()
        
        # ===== ارسال پیام موفقیت با کارت شناسایی =====
        await query.edit_message_text(
            get_register_success_message(temp_username, class_key, Config.STARTING_GOLD)
        )
        
    except Exception as e:
        session.rollback()
        session.close()
        logger.error(f"❌ Error registering user: {e}")
        await query.edit_message_text(
            "❌ **خطا در ثبت‌نام!**\n"
            "لطفاً دوباره با `/register` تلاش کن."
        )

# ============================================
# ۴. لغو ثبت‌نام (اختیاری)
# ============================================

async def cancel_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    لغو فرآیند ثبت‌نام و پاک کردن داده‌های موقت
    """
    user_id = str(update.effective_user.id)
    
    # پاک کردن از لیست انتظار
    if user_id in waiting_for_name:
        del waiting_for_name[user_id]
    
    # پاک کردن از context
    if 'temp_username' in context.user_data:
        context.user_data.pop('temp_username')
    
    await update.message.reply_text(
        "❌ **ثبت‌نام لغو شد.**\n\n"
        "هر وقت آماده بودی، با `/register` دوباره شروع کن.\n"
        "⏳ منتظرت هستیم!"
    )
