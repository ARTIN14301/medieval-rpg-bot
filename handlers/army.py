# handlers/army.py
# ============================================
# سیستم مدیریت ارتش
# ============================================

import logging
from datetime import datetime
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

async def reply(update: Update, text: str):
    await update.message.reply_text(text, parse_mode="MarkdownV2")

async def reply_callback(query, text: str):
    await query.edit_message_text(text, parse_mode="MarkdownV2")

# ============================================
# ۱. انتخاب ارتش
# ============================================

async def chosearmy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    logger.info(f"🔵 chosearmy called for user {user_id}")
    
    session = get_session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    session.close()
    
    if not user:
        await reply(update, "❌ **اول ثبت‌نام کن!**\nبا `/register` شروع کن.")
        return
    
    if user.army and user.army_join_time:
        cooldown_hours = Config.ARMY_CHANGE_COOLDOWN / 3600
        time_passed = (datetime.utcnow() - user.army_join_time).total_seconds() / 3600
        
        if time_passed < cooldown_hours:
            remaining = cooldown_hours - time_passed
            await reply(update, get_army_cooldown_message(remaining))
            return
    
    await update.message.reply_text(
        get_army_selection_message(),
        reply_markup=InlineKeyboardMarkup(get_army_keyboard()),
        parse_mode="MarkdownV2"
    )

# ============================================
# ۲. پردازش انتخاب ارتش
# ============================================

async def army_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    army_key = query.data.replace("army_", "")
    
    logger.info(f"🔵 army_callback called for user {user_id} with army {army_key}")
    
    if army_key not in ARMIES:
        await reply_callback(query, "❌ **ارتش نامعتبر!**\nلطفاً دوباره با `/chosearmy` تلاش کن.")
        return
    
    session = get_session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    
    if not user:
        session.close()
        await reply_callback(query, "❌ **اول ثبت‌نام کن!**\nبا `/register` شروع کن.")
        return
    
    if user.army and user.army_join_time:
        cooldown_hours = Config.ARMY_CHANGE_COOLDOWN / 3600
        time_passed = (datetime.utcnow() - user.army_join_time).total_seconds() / 3600
        
        if time_passed < cooldown_hours:
            remaining = cooldown_hours - time_passed
            session.close()
            await reply_callback(query, get_army_cooldown_message(remaining))
            return
    
    user.army = army_key
    user.army_join_time = datetime.utcnow()
    session.commit()
    session.close()
    
    await reply_callback(query, get_army_join_success_message(army_key))

# ============================================
# ۳. خروج از ارتش
# ============================================

async def leavearmy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    logger.info(f"🔵 leavearmy called for user {user_id}")
    
    session = get_session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    session.close()
    
    if not user:
        await reply(update, "❌ **اول ثبت‌نام کن!**\nبا `/register` شروع کن.")
        return
    
    if not user.army:
        await reply(update, "❌ **تو عضو هیچ ارتشی نیستی!**\nبا `/chosearmy` به یک ارتش بپیوند.")
        return
    
    if user.army_join_time:
        cooldown_hours = Config.ARMY_CHANGE_COOLDOWN / 3600
        time_passed = (datetime.utcnow() - user.army_join_time).total_seconds() / 3600
        
        if time_passed < cooldown_hours:
            remaining = cooldown_hours - time_passed
            await reply(update, f"⏳ **صبر کن!**\n\nتازه به ارتش پیوستی!\n⏱️ **{remaining:.1f} ساعت** دیگه می‌تونی خارج شی.\n\n🛡️ فعلاً با هم‌رزمانت بجنگ!")
            return
    
    session = get_session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    user.army = None
    user.army_join_time = None
    session.commit()
    session.close()
    
    await reply(update, get_army_leave_success_message())
