# utils/messages.py
# ============================================
# همه پیام‌های بات با طراحی حرفه‌ای (MarkdownV2)
# ============================================

from telegram import InlineKeyboardButton
from utils.constants import CLASSES, ARMIES

def get_start_message():
    return (
        "⚔️🏰 **به سرزمین Medieval خوش آمدی، ماجراجو\!** 🏰⚔️\n\n"
        "اینجا جاییه که قهرمان‌ها متولد می‌شن و افسانه‌ها ساخته می‌شن\.\n"
        "آماده‌ای تا نامت در تاریخ ثبت بشه؟\n\n"
        "📜 **برای شروع، یکی از راه‌ها رو انتخاب کن:**\n\n"
        "🟢 `/register` \- ثبت‌نام و شروع ماجراجویی\n"
        "🟡 `/help` \- مشاهده راهنما\n"
        "🔴 `/about` \- درباره بازی"
    )

def get_register_name_message():
    return (
        "📝✨ **گام اول: انتخاب هویت تو**\n\n"
        "یک اسم برای شخصیت خود انتخاب کن:\n"
        "• حداکثر **۱۵** حرف\n"
        "• فقط حروف انگلیسی، اعداد و «_»\n"
        "• این اسم، هویت تو در این دنیاست\n\n"
        "🎯 **مثال:** `ArashTheGreat`\n\n"
        "🔹 **نکته:** این اسم رو نمی‌تونی عوض کنی، پس با دقت انتخابش کن\!\n\n"
        "✏️ لطفاً اسم خود را وارد کن:"
    )

def get_register_class_message():
    return (
        "🎭✨ **گام دوم: انتخاب سرنوشت تو**\n\n"
        "هر کلاس، مسیر متفاوتی در این دنیا داره\. کدوم یکی به تو می‌آید؟\n\n"
        "🟥 **جنگجو** \| 💪 قدرت خالص\n"
        "🟧 **کماندار** \| 🏹 سرعت و دقت\n"
        "🟨 **مدافع** \| 🛡️ زره پولادین\n"
        "🟪 **آسـاسین** \| 🗡️ سایه و ثروت\n\n"
        "🔍 **هر کلاس رو که انتخاب کنی، مزایای خاص خودش رو داری\.**\n\n"
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
        f"✅🎉 **تبریک، ماجراجو\!** 🎉✅\n\n"
        f"تو با موفقیت در دنیای Medieval ثبت‌نام کردی\.\n\n"
        f"📜 **کارت شناسایی تو:**\n"
        f"┌────────────────────────┐\n"
        f"│ 👤 اسم: {username}\n"
        f"│ 🎭 کلاس: {cls['emoji']} {cls['name']}\n"
        f"│ 💰 طلا: {gold}\n"
        f"│ 🌟 لول: ۱\n"
        f"│ 🏅 لقب: کهنه‌سرباز\n"
        f"└────────────────────────┘\n\n"
        f"🛣️ **مراحل بعدی:**\n"
        f"🟢 `/profile` \- مشاهده پروفایل\n"
        f"🔵 `/chosearmy` \- انتخاب ارتش\n"
        f"🔴 `/solofight` \- ورود به نبرد\n\n"
        f"⚔️ **به جمع قهرمانان خوش آمدی\!**"
    )

def get_army_selection_message():
    return (
        "⚔️🛡️ **گام سوم: انتخاب ارتش** 🛡️⚔️\n\n"
        "هر ارتش قدرت و تاریخ خاص خودش رو داره\.\n"
        "انتخاب تو تعیین می‌کنه که در کدام جبهه بجنگی\!\n\n"
        "🟡 **امپراتوری بیزانس** \| 🛡️ دفاع \+۸%\n"
        "🔴 **امپراتوری مقدس روم** \| ⚔️ قدرت \+۷%\n"
        "🟢 **شاهنشاهی ایران** \| 🦁 سرعت \+۵%\n"
        "🟣 **ایلخانان مغول** \| 🏹 قدرت \+۱۰%\n\n"
        "🗡️ لطفاً ارتش خود را انتخاب کن:"
    )

def get_army_join_success_message(army_key):
    army = ARMIES[army_key]
    return (
        f"✅⚔️ **به ارتش {army['name']} پیوستی\!** ⚔️✅\n\n"
        f"{army['emoji']} **بونوس:** \+{army['bonus']}% قدرت\n\n"
        f"🛡️ حالا آماده‌ای تا در کنار هم‌رزمانت بجنگی\!\n"
        f"🔹 با `/solofight` وارد نبرد شو\n"
        f"🔹 با `/profile` پروفایل خود را ببین"
    )

def get_army_leave_success_message():
    return (
        "❌⚔️ **تو از ارتش خارج شدی\!** ⚔️❌\n\n"
        "🛡️ حالا بدون ارتش هستی\.\n"
        "🔹 با `/chosearmy` می‌تونی دوباره به یک ارتش بپیوندی\.\n"
        "⚠️ **یادت باشه:** تا ۴۸ ساعت نمی‌تونی به ارتش جدید بپیوندی\."
    )

def get_army_cooldown_message(hours):
    return (
        f"⏳ **صبر کن\!**\n\n"
        f"تازه ارتش رو عوض کردی\!\n"
        f"⏱️ **{hours:.1f} ساعت** دیگه می‌تونی دوباره عوض کنی\.\n\n"
        f"🛡️ فعلاً با هم‌رزمانت بجنگ\!"
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
