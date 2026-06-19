# handlers/fight.py
# ============================================
# سیستم جنگ کامل - نسخه نهایی با همه چیز
# ============================================

import logging
import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database.db import get_session
from database.schema import User, FightHistory
from utils.constants import get_title
from utils.helpers import get_user_power, get_user_speed
from config import Config

logger = logging.getLogger(__name__)

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
    
    # ===== چک کردن بلاک بعد از باخت (۳۰ دقیقه) =====
    last_fight = session.query(FightHistory).filter_by(
        user_id=user.id, result="lose"
    ).order_by(FightHistory.timestamp.desc()).first()
    
    if last_fight:
        block_time = last_fight.timestamp + timedelta(seconds=Config.FIGHT_BLOCK_DURATION)
        if datetime.utcnow() < block_time:
            remaining = int((block_time - datetime.utcnow()).seconds / 60)
            await update.message.reply_text(
                f"⏳ **{remaining} دقیقه** دیگه می‌تونی بجنگی! (بلاک بعد از باخت)",
                parse_mode="HTML"
            )
            session.close()
            return
    
    session.close()
    
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
    
    # برگشت به پنل اصلی
    if action == "fight_back":
        session = get_session()
        user = session.query(User).filter_by(telegram_id=user_id).first()
        session.close()
        
        if not user:
            await query.edit_message_text("❌ **خطا!**", parse_mode="HTML")
            if user_id in active_panels:
                del active_panels[user_id]
            return
        
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
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
        return
    
    # چک کردن مالکیت پنل
    if user_id not in active_panels:
        await query.edit_message_text("❌ **این پنل منقضی شده!**", parse_mode="HTML")
        return
    
    # اگر کالبک با `fight_level_` شروع شد، بفرست به تابع سطح
    if action.startswith("fight_level_"):
        await fight_level_callback(update, context)
        return
    
    # استخراج نوع جنگ
    fight_type = action.replace("fight_", "")
    
    # ===== چک کردن لول مورد نیاز =====
    level_requirements = {
        "village": 1,
        "army": 7,
        "monster": 15
    }
    
    session = get_session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    session.close()
    
    if not user:
        await query.edit_message_text("❌ **خطا!**", parse_mode="HTML")
        return
    
    if user.level < level_requirements.get(fight_type, 1):
        await query.edit_message_text(
            f"❌ **برای {fight_type} به لول {level_requirements[fight_type]} نیاز داری!**\n"
            f"لول فعلی: {user.level}",
            parse_mode="HTML"
        )
        return
    
    # ===== چک کردن کول‌داون =====
    cooldown_map = {
        "village": Config.FIGHT_COOLDOWN_VILLAGE,
        "army": Config.FIGHT_COOLDOWN_ARMY,
        "monster": Config.FIGHT_COOLDOWN_MONSTER
    }
    
    session = get_session()
    last_fight = session.query(FightHistory).filter_by(
        user_id=user.id, fight_type=fight_type
    ).order_by(FightHistory.timestamp.desc()).first()
    session.close()
    
    if last_fight:
        elapsed = (datetime.utcnow() - last_fight.timestamp).total_seconds()
        cooldown = cooldown_map.get(fight_type, 1800)
        
        # اعمال سرعت روی کول‌داون
        speed = get_user_speed(user)
        reduction = min(50, speed)
        final_cooldown = max(300, cooldown * (1 - reduction / 100))
        
        if elapsed < final_cooldown:
            remaining = int((final_cooldown - elapsed) / 60)
            await query.edit_message_text(
                f"⏳ **{remaining} دقیقه** دیگه می‌تونی {fight_type} بزنی!",
                parse_mode="HTML"
            )
            return
    
    # نمایش سطوح
    rewards = Config.FIGHT_REWARDS.get(fight_type, {})
    if not rewards:
        await query.edit_message_text(f"❌ **نوع جنگ `{fight_type}` نامعتبر!**", parse_mode="HTML")
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
# ۳. شروع جنگ (پردازش سطح انتخاب شده)
# ============================================

async def fight_level_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    
    if user_id not in active_panels:
        await query.edit_message_text("❌ **پنل منقضی شده!**", parse_mode="HTML")
        return
    
    # استخراج اطلاعات
    parts = query.data.split("_")
    if len(parts) != 4:
        await query.edit_message_text("❌ **خطا در دریافت اطلاعات!**", parse_mode="HTML")
        return
    
    fight_type = parts[2]
    try:
        level = int(parts[3])
    except ValueError:
        await query.edit_message_text("❌ **سطح نامعتبر!**", parse_mode="HTML")
        return
    
    session = get_session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    
    if not user:
        await query.edit_message_text("❌ **خطا!**", parse_mode="HTML")
        session.close()
        if user_id in active_panels:
            del active_panels[user_id]
        return
    
    # ===== محاسبه قدرت =====
    user_power = get_user_power(user)
    
    # قدرت دشمن بر اساس نوع جنگ و سطح (بالانس شده)
    base_power = {
        "village": 10,
        "army": 20,
        "monster": 40
    }
    enemy_power = base_power.get(fight_type, 10) + (level * 8) + random.randint(-5, 5)
    enemy_power = max(5, enemy_power)
    
    # شانس پیروزی
    chance = int((user_power / (user_power + enemy_power)) * 100) if (user_power + enemy_power) > 0 else 50
    chance = max(5, min(95, chance))
    
    roll = random.randint(1, 100)
    win = roll <= chance
    
    reward = Config.FIGHT_REWARDS.get(fight_type, {}).get(level, {})
    gold = reward.get("gold", 0)
    exp = reward.get("exp", 0)
    
    # ===== ذخیره تاریخچه =====
    history = FightHistory(
        user_id=user.id,
        fight_type=fight_type,
        fight_level=level,
        result="win" if win else "lose",
        gold_reward=gold if win else 0,
        exp_reward=exp if win else 0
    )
    session.add(history)
    
    if win:
        user.gold += gold
        user.exp += exp
        while user.exp >= user.exp_needed:
            user.exp -= user.exp_needed
            user.level += 1
            user.exp_needed = int(user.exp_needed * 1.2)
            user.title = get_title(user.level)
        
        result_text = (
            f"🎉 **پیروزی!** 🎉\n\n"
            f"💰 +{gold} طلا\n"
            f"✨ +{exp} تجربه\n"
            f"🎲 شانس: {chance}%\n"
            f"⚔️ قدرت شما: {user_power} | قدرت دشمن: {enemy_power}"
        )
    else:
        result_text = (
            f"💀 **شکست!** 💀\n\n"
            f"⏳ {Config.FIGHT_BLOCK_DURATION//60} دقیقه بلاک شدی\n"
            f"🎲 شانس: {chance}%\n"
            f"⚔️ قدرت شما: {user_power} | قدرت دشمن: {enemy_power}"
        )
    
    session.commit()
    session.close()
    
    # حذف پنل
    if user_id in active_panels:
        del active_panels[user_id]
    
    await query.edit_message_text(result_text, parse_mode="HTML")
