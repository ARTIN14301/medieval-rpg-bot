# handlers/register.py
# ============================================
# سیستم ثبت‌نام کامل
# ============================================

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database.db import get_session
from database.schema import User
from utils.constants import CLASSES, get_title
from config import Config

logger = logging.getLogger(__name__)

# دیکشنری برای ذخیره موقت اسم کاربر در حال ثبت‌نام
waiting_for_name = {}

# ============================================
# ۱. شروع ثبت‌نام
# ============================================

async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """شروع فرآیند ثبت‌نام"""
    user_id = str(update.effective_user.id)
    
    # چک کردن اینکه قبلاً ثبت‌نام نکرده
    session = get_session()
    existing = session.query(User).filter_by(telegram_id=user_id).first()
    session.close()
    
    if existing:
        await update.message.reply_text(
            "❌ شما قبلاً ثبت‌نام کرده‌اید!\n"
            f"👤 اسم شما: {existing.username}"
        )
        return
    
    # افزودن کاربر به لیست انتظار
    waiting_for_name[user_id] = True
    
    await update.message.reply_text(
        "📝 **مرحله ۱: انتخاب اسم**\n\n"
        "یک اسم برای شخصیت خود انتخاب کنید:\n"
        "• حداکثر **۱۵** حرف\n"
        "• فقط حروف انگلیسی، اعداد و `_`\n"
        "• نباید تکراری باشد\n\n"
        "مثال: `ArashTheGreat` یا `NightLord`"
    )

# ============================================
# ۲. دریافت اسم و ذخیره موقت
# ============================================

async def handle_name_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دریافت اسم از کاربر و ذخیره موقت"""
    user_id = str(update.effective_user.id)
    
    # چک کردن اینکه کاربر در حالت ثبت‌نام هست
    if user_id not in waiting_for_name:
        return
    
    name = update.message.text.strip()
    
    # اعتبارسنجی اسم
    if len(name) > 15:
        await update.message.reply_text(
            "❌ اسم خیلی بلند است! (حداکثر ۱۵ حرف)\n"
            "لطفاً دوباره تلاش کن:"
        )
        return
    
    if " " in name:
        await update.message.reply_text(
            "❌ اسم نباید فاصله داشته باشد!\n"
            "لطفاً دوباره تلاش کن:"
        )
        return
    
    if not name.replace("_", "").isalnum():
        await update.message.reply_text(
            "❌ فقط حروف انگلیسی، اعداد و `_` مجاز است!\n"
            "لطفاً دوباره تلاش کن:"
        )
        return
    
    # چک کردن تکراری نبودن اسم
    session = get_session()
    existing = session.query(User).filter_by(username=name).first()
    session.close()
    
    if existing:
        await update.message.reply_text(
            f"❌ اسم `{name}` قبلاً استفاده شده!\n"
            "لطفاً اسم دیگری انتخاب کن:"
        )
        return
    
    # ذخیره اسم در context
    context.user_data['temp_username'] = name
    
    # حذف از لیست انتظار
    del waiting_for_name[user_id]
    
    # رفتن به مرحله انتخاب کلاس
    await show_class_selection(update, context)

# ============================================
# ۳. نمایش کلاس‌ها
# ============================================

async def show_class_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش دکمه‌های انتخاب کلاس"""
    
    keyboard = []
    for key, cls in CLASSES.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{cls['emoji']} {cls['name']}",
                callback_data=f"class_{key}"
            )
        ])
    
    text = (
        "🎭 **مرحله ۲: انتخاب کلاس**\n\n"
        "هر کلاس مزایای خاص خود را دارد:\n"
        "🔹 جنگجو: قدرت خالص\n"
        "🔹 کماندار: سرعت و دقت\n"
        "🔹 مدافع: مقاومت بالا\n"
        "🔹 آسـاسین: ترکیبی از قدرت و ثروت\n\n"
        "لطفاً کلاس خود را انتخاب کنید:"
    )
    
    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ============================================
# ۴. انتخاب کلاس و ذخیره نهایی
# ============================================

async def class_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش انتخاب کلاس و ثبت نهایی کاربر"""
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    class_key = query.data.replace("class_", "")
    
    # چک کردن اینکه کلاس معتبر است
    if class_key not in CLASSES:
        await query.edit_message_text("❌ کلاس نامعتبر!")
        return
    
    # دریافت اسم موقت
    temp_username = context.user_data.get('temp_username')
    if not temp_username:
        await query.edit_message_text(
            "❌ خطا! لطفاً دوباره با /register شروع کن."
        )
        return
    
    # چک کردن دوباره تکراری نبودن اسم
    session = get_session()
    existing = session.query(User).filter_by(username=temp_username).first()
    if existing:
        await query.edit_message_text(
            f"❌ اسم `{temp_username}` بین مراحل ثبت‌نام گرفته شده!\n"
            "لطفاً با /register دوباره شروع کن."
        )
        session.close()
        return
    
    # ایجاد کاربر جدید
    new_user = User(
        telegram_id=user_id,
        username=temp_username,
        class_name=class_key,
        level=1,
        title=get_title(1),
        exp=0,
        exp_needed=100,
        gold=Config.STARTING_GOLD,
        wins=0,
        losses=0
    )
    
    session.add(new_user)
    session.commit()
    
    # دریافت اطلاعات کلاس برای پیام نهایی
    cls = CLASSES[class_key]
    
    # پاک کردن داده‌های موقت
    context.user_data.pop('temp_username', None)
    session.close()
    
    # پیام موفقیت
    await query.edit_message_text(
        f"✅ **ثبت‌نام با موفقیت انجام شد!** ✅\n\n"
        f"👤 **اسم:** {temp_username}\n"
        f"🎭 **کلاس:** {cls['emoji']} {cls['name']}\n"
        f"💰 **طلای اولیه:** {Config.STARTING_GOLD} سکه\n"
        f"🌟 **لول:** ۱\n"
        f"🏅 **لقب:** کهنه‌سرباز\n\n"
        "🔰 **مرحله بعدی:**\n"
        "• با `/chosearmy` به یک ارتش بپیوند\n"
        "• با `/solofight` وارد جنگ شو\n"
        "• با `/profile` پروفایل خود را ببین"
    )

# ============================================
# ۵. هندلر لغو (اختیاری)
# ============================================

async def cancel_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لغو فرآیند ثبت‌نام"""
    user_id = str(update.effective_user.id)
    
    if user_id in waiting_for_name:
        del waiting_for_name[user_id]
    
    if 'temp_username' in context.user_data:
        context.user_data.pop('temp_username')
    
    await update.message.reply_text(
        "❌ ثبت‌نام لغو شد.\n"
        "هر وقت آماده بودی با /register دوباره شروع کن."
    )
