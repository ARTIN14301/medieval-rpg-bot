# utils/helpers.py
# ============================================
# توابع کمکی
# ============================================

import random
import re
from datetime import datetime, timedelta
from utils.constants import get_title, ITEMS, ARMIES, CLASSES

def calculate_power(user):
    """محاسبه قدرت کل کاربر"""
    power = 0
    
    # بونوس کلاس
    class_bonus = CLASSES.get(user.class_name, {}).get("bonus", {}).get("power", 0)
    power += class_bonus
    
    # تجهیزات
    if user.current_weapon:
        power += ITEMS.get(user.current_weapon, {}).get("effect", 0)
    if user.current_armor:
        power += ITEMS.get(user.current_armor, {}).get("effect", 0)
    if user.current_horse:
        power += ITEMS.get(user.current_horse, {}).get("effect", 0)
    
    # بونوس ارتش
    if user.army:
        power += ARMIES.get(user.army, {}).get("bonus", 0)
    
    # بونوس لول (هر لول ۱ قدرت)
    power += user.level
    
    return power

def calculate_exp_needed(level):
    """محاسبه تجربه مورد نیاز برای لول بعدی"""
    return int(100 * (1.2 ** (level - 1)))

def check_cooldown(last_time, cooldown_seconds):
    """بررسی کول‌داون"""
    if not last_time:
        return True, 0
    elapsed = (datetime.utcnow() - last_time).total_seconds()
    if elapsed >= cooldown_seconds:
        return True, 0
    return False, cooldown_seconds - elapsed

def paginate(items, page, per_page=5):
    """صفحه‌بندی لیست"""
    start = page * per_page
    end = start + per_page
    return items[start:end], (len(items) + per_page - 1) // per_page

def get_class_emoji(class_name):
    """دریافت ایموجی کلاس"""
    return CLASSES.get(class_name, {}).get("emoji", "❓")

def format_number(num):
    """فرمت‌بندی اعداد با کاما"""
    return f"{num:,}".replace(",", "٬")

def get_user_display_name(user):
    """دریافت نام نمایشی کاربر با کلاس"""
    emoji = get_class_emoji(user.class_name)
    return f"{emoji} {user.username}"

def calculate_fight_risk(user_power, enemy_power, base_risk):
    """محاسبه شانس شکست در جنگ"""
    total_power = user_power + enemy_power
    if total_power == 0:
        return base_risk
    reduction = int((user_power / total_power) * 100)
    risk = max(5, min(95, base_risk - reduction))
    return risk

def get_random_quests(count=3):
    """دریافت کوئست‌های تصادفی"""
    from utils.constants import QUESTS
    return random.sample(QUESTS, min(count, len(QUESTS)))


# utils/helpers.py
# ============================================
# توابع کمکی
# ============================================



# utils/helpers.py
# ============================================
# توابع کمکی
# ============================================



def escape_markdown(text: str) -> str:
    """
    Escape کردن کاراکترهای خاص MarkdownV2
    کاراکترهای خاص: _ * [ ] ( ) ~ ` > # + - = | { } . !
    """
    escape_chars = r'_*[]()~`>#+-=|{}.!'  # <-- ! رو اضافه کردم
    return re.sub(r'([{}])'.format(re.escape(escape_chars)), r'\\\1', text)
