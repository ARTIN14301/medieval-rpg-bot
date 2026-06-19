# handlers/fight.py
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database.db import get_session
from database.schema import User, ActiveFight, FightHistory
from utils.fight_utils import get_user_power, get_user_speed, get_user_defense, calculate_cooldown, calculate_win_chance
from config import Config
import random

logger = logging.getLogger(__name__)
user_fight_panels = {}  # کاربر -> message_id

async def send_fight_panel(update, context, user):
    """ارسال پنل اصلی جنگ"""
    keyboard = [
        [InlineKeyboardButton("🏘️ روستاها (لول ۱+)", callback_data="fight_village")],
        [InlineKeyboardButton("⚔️ ارتش‌ها (لول ۷+)", callback_data="fight_army")],
        [InlineKeyboardButton("👹 هیولاها (لول ۱۵+)", callback_data="fight_monster")],
        [InlineKeyboardButton("❌ بستن", callback_data="fight_close")]
    ]
    
    text = f"⚔️ **سالن جنگ** ⚔️\n\n"
    text += f"🔹 لول: {user.level}\n"
    text += f"⚡ قدرت: {get_user_power(user)}\n"
    text += f"💨 سرعت: {get_user_speed(user)}%\n"
    text += f"🛡️ دفاع: {get_user_defense(user)}%\n\n"
    text += "📋 **دسته‌های موجود:**\n"
    text += "🟢 روستاها (لول ۱+)    ⏳ ۳۰ دقیقه\n"
    text += "🟡 ارتش‌ها (لول ۷+)    ⏳ ۴۵ دقیقه\n"
    text += "🔴 هیولاها (لول ۱۵+)   ⏳ ۶۰ دقیقه"
    
    msg = await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    
    # ذخیره پنل فعال
    session = get_session()
    active = session.query(ActiveFight).filter_by(user_id=user.id).first()
    if active:
        active.message_id = msg.message_id
    else:
        new_active = ActiveFight(user_id=user.id, message_id=msg.message_id)
        session.add(new_active)
    session.commit()
    session.close()
    
    user_fight_panels[str(user.id)] = msg.message_id
    
    # بستن خودکار بعد از ۵ دقیقه
    context.job_queue.run_once(close_fight_panel, 300, data={"user_id": user.id, "chat_id": update.effective_chat.id})

async def close_fight_panel(context):
    data = context.job.data
    user_id = data["user_id"]
    chat_id = data["chat_id"]
    
    if str(user_id) in user_fight_panels:
        del user_fight_panels[str(user_id)]
    
    # پاک کردن از دیتابیس
    session = get_session()
    active = session.query(ActiveFight).filter_by(user_id=user_id).first()
    if active:
        session.delete(active)
        session.commit()
    session.close()
    
    try:
        await context.bot.send_message(chat_id, "⏳ پنل جنگ به دلیل عدم فعالیت بسته شد.")
    except:
        pass

async def solofight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ورود به سالن جنگ"""
    user_id = update.effective_user.id
    session = get_session()
    user = session.query(User).filter_by(telegram_id=str(user_id)).first()
    
    if not user:
        await update.message.reply_text("❌ اول ثبت‌نام کن!")
        return
    
    # چک کردن پنل فعال
    active = session.query(ActiveFight).filter_by(user_id=user.id, status="active").first()
    if active:
        await update.message.reply_text("⏳ شما یک پنل جنگ باز دارید! لطفاً اول آن را ببندید.")
        session.close()
        return
    
    # چک کردن بلاک بعد از باخت
    last_fight = session.query(FightHistory).filter_by(user_id=user.id, result="lose").order_by(FightHistory.timestamp.desc()).first()
    if last_fight:
        block_time = last_fight.timestamp + timedelta(seconds=Config.FIGHT_BLOCK_DURATION)
        if datetime.utcnow() < block_time:
            remaining = int((block_time - datetime.utcnow()).seconds / 60)
            await update.message.reply_text(f"⏳ {remaining} دقیقه دیگه می‌تونی بجنگی!")
            session.close()
            return
    
    session.close()
    await send_fight_panel(update, context, user)

async def fight_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش انتخاب دسته جنگ"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if data == "fight_close":
        await query.edit_message_text("🚪 پنل جنگ بسته شد.")
        user_fight_panels.pop(str(user_id), None)
        session = get_session()
        active = session.query(ActiveFight).filter_by(user_id=user_id).first()
        if active:
            session.delete(active)
            session.commit()
        session.close()
        return
    
    # چک کردن اینکه فقط صاحب پنل دسترسی داشته باشه
    if str(user_id) not in user_fight_panels:
        await query.answer("❌ این پنل متعلق به شما نیست!", show_alert=True)
        return
    
    fight_type = data.replace("fight_", "")
    session = get_session()
    user = session.query(User).filter_by(telegram_id=str(user_id)).first()
    
    if not user:
        await query.edit_message_text("❌ خطا! کاربر پیدا نشد.")
        session.close()
        return
    
    # چک کردن لول
    level_requirements = {"village": 1, "army": 7, "monster": 15}
    if user.level < level_requirements.get(fight_type, 1):
        await query.edit_message_text(f"❌ برای {fight_type} به لول {level_requirements[fight_type]} نیاز داری!")
        session.close()
        return
    
    # چک کردن کول‌داون
    cooldown_map = {
        "village": Config.FIGHT_COOLDOWN_VILLAGE,
        "army": Config.FIGHT_COOLDOWN_ARMY,
        "monster": Config.FIGHT_COOLDOWN_MONSTER
    }
    base_cooldown = cooldown_map.get(fight_type, 1800)
    final_cooldown = calculate_cooldown(base_cooldown, user)
    
    last_fight = session.query(FightHistory).filter_by(user_id=user.id, fight_type=fight_type).order_by(FightHistory.timestamp.desc()).first()
    if last_fight:
        elapsed = (datetime.utcnow() - last_fight.timestamp).total_seconds()
        if elapsed < final_cooldown:
            remaining = int((final_cooldown - elapsed) / 60)
            await query.edit_message_text(f"⏳ {remaining} دقیقه دیگه می‌تونی {fight_type} بزنی!")
            session.close()
            return
    
    # نمایش سطوح
    rewards = Config.FIGHT_REWARDS.get(fight_type, {})
    keyboard = []
    for level, data in rewards.items():
        keyboard.append([InlineKeyboardButton(f"⚔️ {data['name']} (💰{data['gold']} | ✨{data['exp']})", callback_data=f"fight_level_{fight_type}_{level}")])
    keyboard.append([InlineKeyboardButton("🔙 برگشت", callback_data="fight_back")])
    
    await query.edit_message_text(f"⚔️ **{fight_type} - انتخاب سطح:**", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

async def fight_level_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """شروع جنگ با سطح انتخاب شده"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    _, fight_type, level = query.data.split("_")
    level = int(level)
    
    if str(user_id) not in user_fight_panels:
        await query.answer("❌ این پنل متعلق به شما نیست!", show_alert=True)
        return
    
    session = get_session()
    user = session.query(User).filter_by(telegram_id=str(user_id)).first()
    
    if not user:
        await query.edit_message_text("❌ خطا!")
        session.close()
        return
    
    # محاسبه قدرت
    user_power = get_user_power(user)
    enemy_power = random.randint(10, 50) + (level * 5)
    chance = calculate_win_chance(user_power, enemy_power)
    
    # نتیجه
    roll = random.randint(1, 100)
    win = roll <= chance
    
    reward = Config.FIGHT_REWARDS.get(fight_type, {}).get(level, {})
    gold = reward.get("gold", 0)
    exp = reward.get("exp", 0)
    
    if win:
        user.gold += gold
        user.exp += exp
        # چک کردن لول‌آپ
        while user.exp >= user.exp_needed:
            user.exp -= user.exp_needed
            user.level += 1
            user.exp_needed = int(user.exp_needed * 1.2)
            user.title = get_title(user.level)
        
        result_text = f"🎉 **پیروزی!**\n💰 +{gold} طلا\n✨ +{exp} تجربه"
    else:
        result_text = f"💀 **شکست!**\n⏳ {Config.FIGHT_BLOCK_DURATION//60} دقیقه بلاک شدی"
    
    # ذخیره تاریخچه
    history = FightHistory(
        user_id=user.id,
        fight_type=fight_type,
        fight_level=level,
        result="win" if win else "lose",
        gold_reward=gold if win else 0,
        exp_reward=exp if win else 0
    )
    session.add(history)
    session.commit()
    session.close()
    
    # حذف پنل
    user_fight_panels.pop(str(user_id), None)
    await query.edit_message_text(result_text, parse_mode="HTML")
