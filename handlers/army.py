# handlers/army.py
# ============================================
# سیستم مدیریت ارتش
# ============================================

import logging
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database.db import get_session
from database.schema import User
from utils.constants import ARMIES
from utils.messages import (
    get_army_selection_message,
    get_army_join_success_message,
    get_army_leave_success_message,
    get_army_cooldown_message,
    get_army_keyboard
)
from config import Config

logger = logging.getLogger(__name__)

# ============================================
# ۱. انتخاب ارتش
# ============================================

async def chosearmy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    نمایش دکمه‌های انتخاب ارتش
    """
    user_id = str(update.effective_user.id)
    logger.info(f"🔵 chosearmy called for user {user_id}")
    
    # چک کردن ثبت‌نام
    session = get_session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    session.close()
    
    if not user:
        await update.message.reply_text(
            "❌ **اول ثبت‌نام کن!**\n"
            "با `/register` شروع کن."
        )
        return
    
    # چک کردن کول‌داون تغییر ارتش
    if user.army and user.army_join_time:
        cooldown_hours = Config.ARMY_CHANGE_COOLDOWN / 3600
        time_passed = (datetime.utcnow() - user.army_join_time).total_seconds() / 3600
        
        if time_passed < cooldown_hours:
            remaining = cooldown_hours - time_passed
            await update.message.reply_text(
                get_army_cooldown_message(remaining)
            )
            return
    
    # ارسال پیام انتخاب ارتش با دکمه‌ها
    await update.message.reply_text(
        get_army_selection_message(),
        reply_markup=InlineKeyboardMarkup(get_army_keyboard())
    )

# ============================================
# ۲. پردازش انتخاب ارتش
# ============================================

async def army_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    پردازش انتخاب ارتش و ذخیره در دیتابیس
    """
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    army_key = query.data.replace("army_", "")
    
    logger.info(f"🔵 army_callback called for user {user_id} with army {army_key}")
    
    # چک کردن ارتش معتبر
    if army_key not in ARMIES:
        await query.edit_message_text(
            "❌ **ارتش نامعتبر!**\n"
            "لطفاً دوباره با `/chosearmy` تلاش کن."
        )
        return
    
    # چک کردن ثبت‌نام
    session = get_session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    
    if not user:
        session.close()
        await query.edit_message_text(
            "❌ **اول ثبت‌نام کن!**\n"
            "با `/register` شروع کن."
        )
        return
    
    # چک کردن کول‌داون
    if user.army and user.army_join_time:
        cooldown_hours = Config.ARMY_CHANGE_COOLDOWN / 3600
        time_passed = (datetime.utcnow() - user.army_join_time).total_seconds() / 3600
        
        if time_passed < cooldown_hours:
            remaining = cooldown_hours - time_passed
            session.close()
            await query.edit_message_text(
                get_army_cooldown_message(remaining)
            )
            return
    
    # ===== ذخیره ارتش در دیتابیس =====
    user.army = army_key
    user.army_join_time = datetime.utcnow()
    session.commit()
    session.close()
    
    # ارسال پیام موفقیت
    await query.edit_message_text(
        get_army_join_success_message(army_key)
    )

# ============================================
# ۳. خروج از ارتش
# ============================================

async def leavearmy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    خروج از ارتش فعلی با کول‌داون ۴۸ ساعته
    """
    user_id = str(update.effective_user.id)
    logger.info(f"🔵 leavearmy called for user {user_id}")
    
    # چک کردن ثبت‌نام
    session = get_session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    session.close()
    
    if not user:
        await update.message.reply_text(
            "❌ **اول ثبت‌نام کن!**\n"
            "با `/register` شروع کن."
        )
        return
    
    # چک کردن اینکه کاربر ارتش دارد
    if not user.army:
        await update.message.reply_text(
            "❌ **تو عضو هیچ ارتشی نیستی!**\n"
            "با `/chosearmy` به یک ارتش بپیوند."
        )
        return
    
    # ===== چک کردن کول‌داون خروج (۴۸ ساعت) =====
    if user.army_join_time:
        cooldown_hours = Config.ARMY_CHANGE_COOLDOWN / 3600
        time_passed = (datetime.utcnow() - user.army_join_time).total_seconds() / 3600
        
        if time_passed < cooldown_hours:
            remaining = cooldown_hours - time_passed
            await update.message.reply_text(
                f"⏳ **صبر کن!**\n\n"
                f"تازه به ارتش پیوستی!\n"
                f"⏱️ **{remaining:.1f} ساعت** دیگه می‌تونی خارج شی.\n\n"
                f"🛡️ فعلاً با هم‌رزمانت بجنگ!"
            )
            return
    
    # ===== خروج از ارتش =====
    session = get_session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    user.army = None
    user.army_join_time = None
    session.commit()
    session.close()
    
    await update.message.reply_text(
        "❌⚔️ **تو از ارتش خارج شدی!** ⚔️❌\n\n"
        "🛡️ حالا بدون ارتش هستی.\n"
        "🔹 با `/chosearmy` می‌تونی دوباره به یک ارتش بپیوندی."
    )

# ============================================
# ۴. اطلاعات ارتش (برای پروفایل)
# ============================================

def get_user_army_info(user):
    """
    دریافت اطلاعات ارتش کاربر (برای استفاده در پروفایل)
    """
    if not user.army:
        return "ندارد"
    
    army = ARMIES.get(user.army)
    if not army:
        return "نامشخص"
    
    return f"{army['emoji']} {army['name']} (+{army['bonus']}%)"
