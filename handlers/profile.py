# handlers/profile.py
# ============================================
# سیستم پروفایل کاربر
# ============================================

import logging
from telegram import Update
from telegram.ext import ContextTypes

from database.db import get_session
from database.schema import User
from utils.messages import get_profile_message

logger = logging.getLogger(__name__)

async def reply(update: Update, text: str):
    """ارسال پیام با HTML"""
    await update.message.reply_text(text, parse_mode="HTML")

# ============================================
# ۱. نمایش پروفایل
# ============================================

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    نمایش پروفایل کامل کاربر
    """
    user_id = str(update.effective_user.id)
    logger.info(f"🔵 profile called for user {user_id}")
    
    # چک کردن ثبت‌نام
    session = get_session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    session.close()
    
    if not user:
        await reply(update, "❌ <b>اول ثبت‌نام کن!</b>\nبا /register شروع کن.")
        return
    
    # ارسال پیام پروفایل
    await reply(update, get_profile_message(user))
