# utils/fight_utils.py
import random
from datetime import datetime, timedelta
from utils.constants import CLASSES, ARMIES, ITEMS
from config import Config

def get_user_power(user):
    power = user.level * 2
    
    cls = CLASSES.get(user.class_name, {})
    power += cls.get("bonus", {}).get("power", 0)
    
    if user.army:
        army = ARMIES.get(user.army, {})
        power += army.get("bonus", {}).get("power", 0)
    
    # ارتش شخصی (برای بعد)
    # if user.level >= 15 and user.personal_army:
    #     power += user.personal_army_power
    
    if user.current_weapon:
        power += ITEMS.get(user.current_weapon, {}).get("power", 0)
    if user.current_armor:
        power += ITEMS.get(user.current_armor, {}).get("power", 0)
    if user.current_horse:
        power += ITEMS.get(user.current_horse, {}).get("power", 0)
    
    return power

def get_user_speed(user):
    speed = 0
    cls = CLASSES.get(user.class_name, {})
    speed += cls.get("bonus", {}).get("speed", 0)
    
    if user.army:
        army = ARMIES.get(user.army, {})
        speed += army.get("bonus", {}).get("speed", 0)
    
    if user.current_horse:
        speed += ITEMS.get(user.current_horse, {}).get("speed", 0)
    
    return speed

def get_user_defense(user):
    defense = 0
    cls = CLASSES.get(user.class_name, {})
    defense += cls.get("bonus", {}).get("defense", 0)
    
    if user.army:
        army = ARMIES.get(user.army, {})
        defense += army.get("bonus", {}).get("defense", 0)
    
    if user.current_armor:
        defense += ITEMS.get(user.current_armor, {}).get("defense", 0)
    
    return defense

def calculate_cooldown(base_cooldown, user):
    speed = get_user_speed(user)
    reduction = min(50, speed)  # حداکثر ۵۰٪ کاهش
    final_cooldown = base_cooldown * (1 - reduction / 100)
    return max(300, int(final_cooldown))  # حداقل ۵ دقیقه

def calculate_win_chance(user_power, enemy_power):
    total = user_power + enemy_power
    if total == 0:
        return 50
    return int((user_power / total) * 100)
