# handlers/register.py
# ============================================
# سیستم ثبت‌نام کامل با طراحی حرفه‌ای (HTML)
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

waiting_for_name = {}

async def reply(update: Update, text: str):
    """ارسال پیام با HTML"""
    await update.message.reply_text(text, parse_mode="HTML")

async def reply_callback(query, text: str):
    """ویرایش پیام با HTML"""
    await query.edit_message_text(text, parse_mode="HTML")

# ============================================
# ۱. شروع ثبت‌نام
# ============================================

async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    logger.info(f"🔵 register_start called for user {user_id}")
    
    session = get_session()
    existing = session.query(User).filter_by(telegram_id=user_id).first()
    session.close()
    
    if existing:
        await reply(update, f"❌ شما قبلاً با اسم <code>{existing.username}</code> ثبت‌نام کردی!\nبرای مشاهده پروفایل از /profile استفاده کن.")
        return
    
    waiting_for_name[user_id] = True
    await reply(update, get_register_name_message())

# ============================================
# ۲. دریافت اسم
# ============================================

async def handle_name_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    logger.info(f"🔵 handle_name_input called for user {user_id}")
    
    if user_id not in waiting_for_name:
        return
    
    name = update.message.text.strip()
    
    if len(name) > 15:
        await reply(update, "❌ <b>اسم خیلی بلند است!</b>\nحداکثر ۱۵ حرف مجاز است.\n\n✏️ لطفاً دوباره تلاش کن:")
        return
    
    if " " in name:
        await reply(update, "❌ <b>اسم نباید فاصله داشته باشد!</b>\nاز «_» برای جدا کردن کلمات استفاده کن.\n\n✏️ لطفاً دوباره تلاش کن:")
        return
    
    if not name.replace("_", "").isalnum():
        await reply(update, "❌ <b>اسم نامعتبر است!</b>\nفقط حروف انگلیسی، اعداد و «_» مجاز است.\n\n✏️ لطفاً دوباره تلاش کن:")
        return
    
    session = get_session()
    existing = session.query(User).filter_by(username=name).first()
    session.close()
    
    if existing:
        await reply(update, f"❌ <b>اسم <code>{name}</code> قبلاً استفاده شده!</b>\nیک اسم دیگر انتخاب کن.\n\n✏️ لطفاً دوباره تلاش کن:")
        return
    
    context.user_data['temp_username'] = name
    del waiting_for_name[user_id]
    
    await update.message.reply_text(
        get_register_class_message(),
        reply_markup=InlineKeyboardMarkup(get_class_keyboard()),
        parse_mode="HTML"
    )

# ============================================
# ۳. انتخاب کلاس
# ============================================

async def class_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    class_key = query.data.replace("class_", "")
    
    logger.info(f"🔵 class_callback called for user {user_id} with class {class_key}")
    
    if class_key not in CLASSES:
        await reply_callback(query, "❌ <b>کلاس نامعتبر!</b>\nلطفاً با /register دوباره شروع کن.")
        return
    
    temp_username = context.user_data.get('temp_username')
    if not temp_username:
        await reply_callback(query, "❌ <b>خطا!</b>\nلطفاً با /register دوباره شروع کن.")
        return
    
    session = get_session()
    existing = session.query(User).filter_by(username=temp_username).first()
    if existing:
        session.close()
        await reply_callback(query, f"❌ <b>اسم <code>{temp_username}</code> بین مراحل ثبت‌نام گرفته شد!</b>\nلطفاً با /register دوباره شروع کن.")
        return
    
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
        
        context.user_data.pop('temp_username', None)
        session.close()
        
        await reply_callback(query, get_register_success_message(temp_username, class_key, Config.STARTING_GOLD))
        
    except Exception as e:
        session.rollback()
        session.close()
        logger.error(f"❌ Error registering user: {e}")
        await reply_callback(query, "❌ <b>خطا در ثبت‌نام!</b>\nلطفاً دوباره با /register تلاش کن.")

# ============================================
# ۴. لغو ثبت‌نام
# ============================================

async def cancel_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    
    if user_id in waiting_for_name:
        del waiting_for_name[user_id]
    
    if 'temp_username' in context.user_data:
        context.user_data.pop('temp_username')
    
    await reply(update, "❌ <b>ثبت‌نام لغو شد.</b>\n\nهر وقت آماده بودی، با /register دوباره شروع کن.\n⏳ منتظرت هستیم!")
