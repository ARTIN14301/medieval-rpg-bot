# handlers/fight.py
# ============================================
# سیستم جنگ کامل (PvE) - نسخه نهایی
# ============================================

import logging
import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database.db import get_session
from database.schema import User
from utils.constants import get_title
from utils.helpers import get_user_power, get_user_speed, get_user_defense, calculate_cooldown
from config import Config

logger = logging.getLogger(__name__)

# ============================================
# دیکشنری ساده برای پنل‌های فعال (فقط در حافظه)
# ============================================
active_panels = {}

# ============================================
# ۱. نمایش پنل اصلی جنگ
# ============================================

async def solofight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    session = get_session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    
    if not user:
        await update.message.reply_text("❌ **اول ثبت‌نام کن!**", parse_mode="HTML")
        session.close()
        return
    
    # چک کردن پنل فعال
    if user_id in active_panels:
        await update.message.reply_text("⏳ **شما یک پنل جنگ باز دارید!**", parse_mode="HTML")
        session.close()
        return
    
    session.close()
    
    # ساخت پنل
    keyboard = [
        [InlineKeyboardButton("🏘️ روستاها (لول ۱+)", callback_data="fight_village")],
        [InlineKeyboardButton("⚔️ ارتش‌ها (لول ۷+)", callback_data="fight_army")],
        [InlineKeyboardButton("👹 هیولاها (لول ۱۵+)", callback_data="fight_monster")],
        [InlineKeyboardButton("❌ بستن پنل", callback_data="fight_close")]
    ]
    
    text = (
        f"⚔️ **سالن جنگ** ⚔️\n\n"
        f"🔹 لول: {user.level}\n"
        f"⚡ قدرت: {get_user_power(user)}\n"
        f"💨 سرعت: {get_user_speed(user)}%\n\n"
        f"📋 **دسته‌های موجود:**\n"
        f"🟢 روستاها (لول ۱+)    ⏳ ۳۰ دقیقه\n"
        f"🟡 ارتش‌ها (لول ۷+)    ⏳ ۴۵ دقیقه\n"
        f"🔴 هیولاها (لول ۱۵+)   ⏳ ۶۰ دقیقه"
    )
    
    msg = await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )
    
    active_panels[user_id] = msg.message_id

# ============================================
# ۲. کالبک‌های جنگ
# ============================================

async def fight_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    action = query.data
    
    # بستن پنل
    if action == "fight_close":
        if user_id in active_panels:
            del active_panels[user_id]
        await query.edit_message_text("🚪 **پنل جنگ بسته شد.**", parse_mode="HTML")
        return
    
    # چک کردن مالکیت پنل
    if user_id not in active_panels:
        await query.edit_message_text("❌ **این پنل منقضی شده!**", parse_mode="HTML")
        return
    
    # استخراج نوع جنگ
    fight_type = action.replace("fight_", "")
    
    # نمایش سطوح
    rewards = Config.FIGHT_REWARDS.get(fight_type, {})
    if not rewards:
        await query.edit_message_text("❌ **نوع جنگ نامعتبر!**", parse_mode="HTML")
        return
    
    keyboard = []
    for level, data in rewards.items():
        keyboard.append([
            InlineKeyboardButton(
                f"⚔️ {data['name']} (💰{data['gold']} | ✨{data['exp']})",
                callback_data=f"fight_level_{fight_type}_{level}"
            )
        ])
    keyboard.append([InlineKeyboardButton("🔙 برگشت", callback_data="fight_back")])
    
    await query.edit_message_text(
        f"⚔️ **{fight_type} - انتخاب سطح:**",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )

# ============================================
# ۳. شروع جنگ
# ============================================

async def fight_level_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    
    if user_id not in active_panels:
        await query.edit_message_text("❌ **پنل منقضی شده!**", parse_mode="HTML")
        return
    
    _, fight_type, level = query.data.split("_")
    level = int(level)
    
    session = get_session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    
    if not user:
        await query.edit_message_text("❌ **خطا!**", parse_mode="HTML")
        session.close()
        return
    
    # محاسبه قدرت
    user_power = get_user_power(user)
    enemy_power = random.randint(10, 50) + (level * 5)
    chance = int((user_power / (user_power + enemy_power)) * 100) if (user_power + enemy_power) > 0 else 50
    
    roll = random.randint(1, 100)
    win = roll <= chance
    
    reward = Config.FIGHT_REWARDS.get(fight_type, {}).get(level, {})
    gold = reward.get("gold", 0)
    exp = reward.get("exp", 0)
    
    if win:
        user.gold += gold
        user.exp += exp
        # لول‌آپ
        while user.exp >= user.exp_needed:
            user.exp -= user.exp_needed
            user.level += 1
            user.exp_needed = int(user.exp_needed * 1.2)
            user.title = get_title(user.level)
        
        result_text = (
            f"🎉 **پیروزی!** 🎉\n\n"
            f"💰 +{gold} طلا\n"
            f"✨ +{exp} تجربه\n"
            f"🎲 شانس: {chance}%"
        )
    else:
        result_text = (
            f"💀 **شکست!** 💀\n\n"
            f"⏳ {Config.FIGHT_BLOCK_DURATION//60} دقیقه بلاک شدی\n"
            f"🎲 شانس: {chance}%"
        )
    
    session.commit()
    session.close()
    
    # حذف پنل
    if user_id in active_panels:
        del active_panels[user_id]
    
    await query.edit_message_text(result_text, parse_mode="HTML")
