import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db import get_session
from database.schema import User
from utils.constants import CLASSES, get_title
from config import Config

logger = logging.getLogger(__name__)
waiting_for_name = {}

async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🔵 register_start called")
    user_id = str(update.effective_user.id)
    
    session = get_session()
    existing = session.query(User).filter_by(telegram_id=user_id).first()
    session.close()
    
    if existing:
        await update.message.reply_text(f"❌ شما قبلاً ثبت‌نام کرده‌اید!")
        return
    
    waiting_for_name[user_id] = True
    await update.message.reply_text(
        "📝 **مرحله ۱: انتخاب اسم**\n\n"
        "یک اسم برای شخصیت خود انتخاب کنید:\n"
        "• حداکثر ۱۵ حرف\n"
        "• فقط حروف انگلیسی، اعداد و _\n\n"
        "مثال: `ArashTheGreat`"
    )

async def handle_name_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🔵 handle_name_input called")
    user_id = str(update.effective_user.id)
    
    if user_id not in waiting_for_name:
        logger.info(f"User {user_id} not in waiting_for_name")
        return
    
    name = update.message.text.strip()
    
    if len(name) > 15 or " " in name or not name.replace("_", "").isalnum():
        await update.message.reply_text("❌ اسم نامعتبر! دوباره تلاش کن:")
        return
    
    session = get_session()
    existing = session.query(User).filter_by(username=name).first()
    if existing:
        session.close()
        await update.message.reply_text(f"❌ اسم `{name}` قبلاً استفاده شده!")
        return
    
    context.user_data['temp_username'] = name
    del waiting_for_name[user_id]
    
    keyboard = []
    for key, cls in CLASSES.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{cls['emoji']} {cls['name']}",
                callback_data=f"class_{key}"
            )
        ])
    
    await update.message.reply_text(
        "🎭 **مرحله ۲: انتخاب کلاس**",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def class_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🔵 class_callback called")
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    class_key = query.data.replace("class_", "")
    
    if class_key not in CLASSES:
        await query.edit_message_text("❌ کلاس نامعتبر!")
        return
    
    temp_username = context.user_data.get('temp_username')
    if not temp_username:
        await query.edit_message_text("❌ خطا! لطفاً با /register شروع کن.")
        return
    
    session = get_session()
    existing = session.query(User).filter_by(username=temp_username).first()
    if existing:
        session.close()
        await query.edit_message_text(f"❌ اسم `{temp_username}` قبلاً گرفته شده!")
        return
    
    new_user = User(
        telegram_id=user_id,
        username=temp_username,
        class_name=class_key,
        gold=Config.STARTING_GOLD
    )
    session.add(new_user)
    session.commit()
    session.close()
    
    context.user_data.pop('temp_username', None)
    
    cls = CLASSES[class_key]
    await query.edit_message_text(
        f"✅ **ثبت‌نام موفق!**\n\n"
        f"👤 اسم: {temp_username}\n"
        f"🎭 کلاس: {cls['emoji']} {cls['name']}\n"
        f"💰 طلا: {Config.STARTING_GOLD}"
    )
