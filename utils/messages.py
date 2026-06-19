# utils/messages.py
# ============================================
# همه پیام‌های بات با طراحی حرفه‌ای (HTML)
# ============================================

from telegram import InlineKeyboardButton
from utils.constants import CLASSES, ARMIES

def get_start_message():
    return (
        "⚔️🏰 <b>به سرزمین Medieval خوش آمدی، ماجراجو!</b> 🏰⚔️\n\n"
        "اینجا جاییه که قهرمان‌ها متولد می‌شن و افسانه‌ها ساخته می‌شن.\n"
        "آماده‌ای تا نامت در تاریخ ثبت بشه؟\n\n"
        "📜 <b>برای شروع، یکی از راه‌ها رو انتخاب کن:</b>\n\n"
        "🟢 /register - ثبت‌نام و شروع ماجراجویی\n"
        "🟡 /help - مشاهده راهنما\n"
        "🔴 /about - درباره بازی"
    )

def get_register_name_message():
    return (
        "📝✨ <b>گام اول: انتخاب هویت تو</b>\n\n"
        "یک اسم برای شخصیت خود انتخاب کن:\n"
        "• حداکثر <b>۱۵</b> حرف\n"
        "• فقط حروف انگلیسی، اعداد و «_»\n"
        "• این اسم، هویت تو در این دنیاست\n\n"
        "🎯 <b>مثال:</b> <code>ArashTheGreat</code>\n\n"
        "🔹 <b>نکته:</b> این اسم رو نمی‌تونی عوض کنی، پس با دقت انتخابش کن!\n\n"
        "✏️ لطفاً اسم خود را وارد کن:"
    )

def get_register_class_message():
    return (
        "🎭✨ <b>گام دوم: انتخاب سرنوشت تو</b>\n\n"
        "هر کلاس، مسیر متفاوتی در این دنیا داره. کدوم یکی به تو می‌آید؟\n\n"
        "🟥 <b>جنگجو</b> | 💪 قدرت خالص\n"
        "🟧 <b>کماندار</b> | 🏹 سرعت و دقت\n"
        "🟨 <b>مدافع</b> | 🛡️ زره پولادین\n"
        "🟪 <b>آسـاسین</b> | 🗡️ سایه و ثروت\n\n"
        "🔍 <b>هر کلاس رو که انتخاب کنی، مزایای خاص خودش رو داری.</b>\n\n"
        "🗡️ لطفاً کلاس خود را انتخاب کن:"
    )

def get_class_keyboard():
    return [
        [InlineKeyboardButton("🟥 جنگجو", callback_data="class_warrior")],
        [InlineKeyboardButton("🟧 کماندار", callback_data="class_archer")],
        [InlineKeyboardButton("🟨 مدافع", callback_data="class_defender")],
        [InlineKeyboardButton("🟪 آسـاسین", callback_data="class_assassin")]
    ]

def get_register_success_message(username, class_key, gold):
    cls = CLASSES[class_key]
    return (
        f"✅🎉 <b>تبریک، ماجراجو!</b> 🎉✅\n\n"
        f"تو با موفقیت در دنیای Medieval ثبت‌نام کردی.\n\n"
        f"📜 <b>کارت شناسایی تو:</b>\n"
        f"┌────────────────────────┐\n"
        f"│ 👤 اسم: {username}\n"
        f"│ 🎭 کلاس: {cls['emoji']} {cls['name']}\n"
        f"│ 💰 طلا: {gold}\n"
        f"│ 🌟 لول: ۱\n"
        f"│ 🏅 لقب: کهنه‌سرباز\n"
        f"└────────────────────────┘\n\n"
        f"🛣️ <b>مراحل بعدی:</b>\n"
        f"🟢 /profile - مشاهده پروفایل\n"
        f"🔵 /chosearmy - انتخاب ارتش\n"
        f"🔴 /solofight - ورود به نبرد\n\n"
        f"⚔️ <b>به جمع قهرمانان خوش آمدی!</b>"
    )

def get_army_selection_message():
    return (
        "⚔️🛡️ <b>گام سوم: انتخاب ارتش</b> 🛡️⚔️\n\n"
        "هر ارتش قدرت و تاریخ خاص خودش رو داره.\n"
        "انتخاب تو تعیین می‌کنه که در کدام جبهه بجنگی!\n\n"
        "🟡 <b>امپراتوری بیزانس</b> | 🛡️ دفاع +۸%\n"
        "🔴 <b>امپراتوری مقدس روم</b> | ⚔️ قدرت +۷%\n"
        "🟢 <b>شاهنشاهی ایران</b> | 🦁 سرعت +۵%\n"
        "🟣 <b>ایلخانان مغول</b> | 🏹 قدرت +۱۰%\n\n"
        "🗡️ لطفاً ارتش خود را انتخاب کن:"
    )

def get_army_join_success_message(army_key):
    army = ARMIES[army_key]
    return (
        f"✅⚔️ <b>به ارتش {army['name']} پیوستی!</b> ⚔️✅\n\n"
        f"{army['emoji']} <b>بونوس:</b> +{army['bonus']}% قدرت\n\n"
        f"🛡️ حالا آماده‌ای تا در کنار هم‌رزمانت بجنگی!\n"
        f"🔹 با /solofight وارد نبرد شو\n"
        f"🔹 با /profile پروفایل خود را ببین"
    )

def get_army_leave_success_message():
    return (
        "❌⚔️ <b>تو از ارتش خارج شدی!</b> ⚔️❌\n\n"
        "🛡️ حالا بدون ارتش هستی.\n"
        "🔹 با /chosearmy می‌تونی دوباره به یک ارتش بپیوندی.\n"
        "⚠️ <b>یادت باشه:</b> تا ۴۸ ساعت نمی‌تونی به ارتش جدید بپیوندی."
    )

def get_army_cooldown_message(hours):
    return (
        f"⏳ <b>صبر کن!</b>\n\n"
        f"تازه ارتش رو عوض کردی!\n"
        f"⏱️ <b>{hours:.1f} ساعت</b> دیگه می‌تونی دوباره عوض کنی.\n\n"
        f"🛡️ فعلاً با هم‌رزمانت بجنگ!"
    )

def get_army_keyboard():
    keyboard = []
    for key, army in ARMIES.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{army['emoji']} {army['name']}",
                callback_data=f"army_{key}"
            )
        ])
    return keyboard



# ============================================
# پیام پروفایل
# ============================================

def get_profile_message(user):
    """
    ساخت پیام پروفایل کاربر
    """
    # اطلاعات کلاس
    cls = CLASSES.get(user.class_name, {})
    class_name = cls.get("name", "نامشخص")
    class_emoji = cls.get("emoji", "❓")
    
    # اطلاعات ارتش
    army_name = "ندارد"
    army_emoji = ""
    army_bonus = 0
    if user.army:
        army = ARMIES.get(user.army, {})
        army_name = army.get("name", "نامشخص")
        army_emoji = army.get("emoji", "")
        army_bonus = army.get("bonus", 0)
    
    # محاسبه قدرت کل
    from utils.helpers import get_user_power
    power = get_user_power(user)
    
    # ساخت پیام
    text = (
        f"📜 <b>کارت شناسایی {user.username}</b> 📜\n\n"
        f"┌─────────────────────────────┐\n"
        f"│ 🎭 <b>کلاس:</b> {class_emoji} {class_name}\n"
        f"│ 🌟 <b>لول:</b> {user.level}\n"
        f"│ 🏅 <b>لقب:</b> {user.title}\n"
        f"│ 💰 <b>طلا:</b> {user.gold:,}\n"
        f"│ ⚔️ <b>قدرت:</b> {power}\n"
        f"│ 🏆 <b>برد:</b> {user.wins}\n"
        f"│ 💀 <b>باخت:</b> {user.losses}\n"
    )
    
    # ارتش
    if user.army:
        text += f"│ ⚔️ <b>ارتش:</b> {army_emoji} {army_name} (+{army_bonus}%)\n"
    else:
        text += f"│ ⚔️ <b>ارتش:</b> {army_name}\n"
    
    # تجهیزات
    from utils.constants import ITEMS
    
    weapon_name = "ندارد"
    weapon_effect = 0
    if user.current_weapon:
        item = ITEMS.get(user.current_weapon, {})
        weapon_name = item.get("name", "نامشخص")
        weapon_effect = item.get("effect", 0)
    text += f"│ 🗡️ <b>سلاح:</b> {weapon_name}"
    if weapon_effect > 0:
        text += f" (+{weapon_effect}%)"
    text += "\n"
    
    armor_name = "ندارد"
    armor_effect = 0
    if user.current_armor:
        item = ITEMS.get(user.current_armor, {})
        armor_name = item.get("name", "نامشخص")
        armor_effect = item.get("effect", 0)
    text += f"│ 🛡️ <b>زره:</b> {armor_name}"
    if armor_effect > 0:
        text += f" (+{armor_effect}%)"
    text += "\n"
    
    horse_name = "ندارد"
    horse_effect = 0
    if user.current_horse:
        item = ITEMS.get(user.current_horse, {})
        horse_name = item.get("name", "نامشخص")
        horse_effect = item.get("effect", 0)
    text += f"│ 🐎 <b>اسب:</b> {horse_name}"
    if horse_effect > 0:
        text += f" (+{horse_effect}%)"
    text += "\n"
    
    text += "└─────────────────────────────┘\n\n"
    
    # نوار پیشرفت
    exp_percent = int((user.exp / user.exp_needed) * 100) if user.exp_needed > 0 else 0
    exp_bar = "█" * (exp_percent // 5) + "░" * (20 - (exp_percent // 5))
    
    text += (
        f"📊 <b>پیشرفت:</b>\n"
        f"┌─────────────────────────────┐\n"
        f"│ {exp_bar}\n"
        f"│ {user.exp} / {user.exp_needed} تجربه\n"
        f"└─────────────────────────────┘\n\n"
    )
    
    # راهنما
    text += (
        f"🛣️ <b>راه‌های پیشرفت:</b>\n"
        f"🔹 با /solofight به جنگ برو\n"
        f"🔹 با /shop تجهیزات بخر\n"
        f"🔹 با /daily کوئست بگیر"
    )
    
    return text
