# utils/helpers.py
# ============================================
# توابع کمکی
# ============================================

from utils.constants import CLASSES, ARMIES, ITEMS

def get_user_power(user):
    """محاسبه قدرت کل کاربر"""
    power = user.level * 2
    
    # کلاس
    cls = CLASSES.get(user.class_name, {})
    power += cls.get("bonus", {}).get("power", 0)
    
    # ارتش دیفالت
    if user.army:
        army = ARMIES.get(user.army, {})
        army_bonus = army.get("bonus", {})
        power += army_bonus.get("power", 0)
    
    # تجهیزات
    if user.current_weapon:
        item = ITEMS.get(user.current_weapon, {})
        power += item.get("power", 0)
    if user.current_armor:
        item = ITEMS.get(user.current_armor, {})
        power += item.get("power", 0)
    if user.current_horse:
        item = ITEMS.get(user.current_horse, {})
        power += item.get("power", 0)
    
    return power

def get_user_speed(user):
    """محاسبه سرعت کاربر"""
    speed = 0
    
    # کلاس
    cls = CLASSES.get(user.class_name, {})
    speed += cls.get("bonus", {}).get("speed", 0)
    
    # ارتش
    if user.army:
        army = ARMIES.get(user.army, {})
        army_bonus = army.get("bonus", {})
        speed += army_bonus.get("speed", 0)
    
    # اسب
    if user.current_horse:
        item = ITEMS.get(user.current_horse, {})
        speed += item.get("speed", 0)
    
    return speed

def get_user_defense(user):
    """محاسبه دفاع کاربر"""
    defense = 0
    
    # کلاس
    cls = CLASSES.get(user.class_name, {})
    defense += cls.get("bonus", {}).get("defense", 0)
    
    # ارتش
    if user.army:
        army = ARMIES.get(user.army, {})
        army_bonus = army.get("bonus", {})
        defense += army_bonus.get("defense", 0)
    
    # زره
    if user.current_armor:
        item = ITEMS.get(user.current_armor, {})
        defense += item.get("defense", 0)
    
    return defense

def calculate_cooldown(base_cooldown, user):
    """محاسبه کول‌داون نهایی با اعمال سرعت"""
    speed = get_user_speed(user)
    reduction = min(50, speed)
    final_cooldown = base_cooldown * (1 - reduction / 100)
    return max(300, int(final_cooldown))
