# utils/constants.py
# ============================================
# ثابت‌های بازی (کلاس‌ها، ارتش‌ها، آیتم‌ها، لقب‌ها)
# ============================================

# ============================================
# ۱. کلاس‌های بازی
# ============================================

CLASSES = {
    "warrior": {
        "name": "جنگجو",
        "emoji": "⚔️",
        "bonus": {"power": 20, "gold": 0, "speed": 0, "defense": 0}
    },
    "archer": {
        "name": "کماندار",
        "emoji": "🏹",
        "bonus": {"power": 15, "gold": 0, "speed": 10, "defense": 0}
    },
    "defender": {
        "name": "مدافع",
        "emoji": "🛡️",
        "bonus": {"power": 0, "gold": 0, "speed": 0, "defense": 20}
    },
    "assassin": {
        "name": "آسـاسین",
        "emoji": "🗡️",
        "bonus": {"power": 5, "gold": 15, "speed": 0, "defense": 0}
    }
}

# ============================================
# ۲. ارتش‌های دیفالت
# ============================================

ARMIES = {
    "byzantine": {
        "name": "بیزانس",
        "emoji": "🛡️",
        "bonus": {"power": 8, "speed": 0, "defense": 5}
    },
    "holy_roman": {
        "name": "روم مقدس",
        "emoji": "⚔️",
        "bonus": {"power": 7, "speed": 0, "defense": 3}
    },
    "persian": {
        "name": "ایران",
        "emoji": "🦁",
        "bonus": {"power": 5, "speed": 5, "defense": 0}
    },
    "mongol": {
        "name": "مغول",
        "emoji": "🏹",
        "bonus": {"power": 10, "speed": 10, "defense": 0}
    }
}

# ============================================
# ۳. لقب‌ها (هر ۲ لول - ۵۰ لقب)
# ============================================

TITLES = {
    1: "کهنه‌سرباز",
    3: "دلاور",
    5: "پهلوان",
    7: "شمشیرزن",
    9: "سردار",
    11: "فاتح",
    13: "نجیب‌زاده",
    15: "فرمانده",
    17: "والی",
    19: "فئودال",
    21: "بارون",
    23: "ویسکونت",
    25: "کنت",
    27: "مارکیز",
    29: "دوک",
    31: "ارل",
    33: "شاهزاده",
    35: "ژنرال",
    37: "مارشال",
    39: "فرمانده کل",
    41: "ارباب شمشیر",
    43: "فاتح سرزمین‌ها",
    45: "پادشاه جنگ",
    47: "امپراتور",
    49: "افسانه",
    51: "فرمانده بزرگ",
    53: "ارباب سپاه‌ها",
    55: "نگهبان کهکشان",
    57: "صاحب تاج و تخت",
    59: "افسانه زنده",
    61: "روح جنگ",
    63: "امپراتور آهن",
    65: "فرمانروای ابدی",
    67: "خدای جنگ",
    69: "جاودانه",
    71: "بی‌نهایت",
    73: "سلطان جهان‌ها",
    75: "افسانه‌وار",
    77: "بی‌همتا",
    79: "بی‌نظیر",
    81: "ایزد جنگ",
    83: "ارباب هستی",
    85: "تجسم قدرت",
    87: "بی‌نهایت بزرگ",
    89: "متعالی",
    91: "بی‌پایان",
    93: "یگانه",
    95: "بی‌مرز",
    97: "مطلق",
    99: "خالق سرنوشت"
}

def get_title(level):
    if level < 1:
        return TITLES[1]
    if level > 99:
        return TITLES[99]
    closest = level if level % 2 == 1 else level - 1
    if closest < 1:
        closest = 1
    return TITLES.get(closest, TITLES[1])

# ============================================
# ۴. آیتم‌های شاپ (۱۵ سلاح، ۱۵ زره، ۵ اسب)
# ============================================

ITEMS = {
    # ===== سلاح‌ها (۱۵ عدد) =====
    "wooden_sword": {"name": "🪵 شمشیر چوبی", "type": "weapon", "price": 500, "power": 1, "speed": 0, "defense": 0},
    "stone_axe": {"name": "🪨 تبر سنگی", "type": "weapon", "price": 1000, "power": 2, "speed": 0, "defense": 0},
    "iron_dagger": {"name": "🔪 خنجر آهنی", "type": "weapon", "price": 2000, "power": 3, "speed": 0, "defense": 0},
    "bronze_sword": {"name": "⚔️ شمشیر برنزی", "type": "weapon", "price": 3500, "power": 4, "speed": 0, "defense": 0},
    "steel_sword": {"name": "🗡️ شمشیر فولادی", "type": "weapon", "price": 5000, "power": 5, "speed": 0, "defense": 0},
    "crimson_blade": {"name": "🔴 تیغ زرشکی", "type": "weapon", "price": 10000, "power": 7, "speed": 0, "defense": 0},
    "shadow_dagger": {"name": "🌑 خنجر سایه", "type": "weapon", "price": 15000, "power": 9, "speed": 0, "defense": 0},
    "dragon_claw": {"name": "🐉 چنگال اژدها", "type": "weapon", "price": 20000, "power": 11, "speed": 0, "defense": 0},
    "thunder_sword": {"name": "⚡ شمشیر رعد", "type": "weapon", "price": 30000, "power": 13, "speed": 0, "defense": 0},
    "frost_blade": {"name": "❄️ تیغ یخی", "type": "weapon", "price": 50000, "power": 16, "speed": 0, "defense": 0},
    "hell_sword": {"name": "🔥 شمشیر جهنم", "type": "weapon", "price": 65000, "power": 19, "speed": 0, "defense": 0},
    "star_breaker": {"name": "⭐ ستاره‌شکن", "type": "weapon", "price": 80000, "power": 22, "speed": 0, "defense": 0},
    "void_sword": {"name": "🌀 شمشیر خلأ", "type": "weapon", "price": 100000, "power": 25, "speed": 0, "defense": 0},
    "soul_reaper": {"name": "💀 دروگر ارواح", "type": "weapon", "price": 150000, "power": 30, "speed": 0, "defense": 0},
    "god_slayer": {"name": "✨ خداکش", "type": "weapon", "price": 200000, "power": 35, "speed": 0, "defense": 0},
    
    # ===== زره‌ها (۱۵ عدد) =====
    "leather_armor": {"name": "🟫 زره چرمی", "type": "armor", "price": 500, "power": 0, "speed": 0, "defense": 1},
    "studded_armor": {"name": "🔘 زره میخی", "type": "armor", "price": 1000, "power": 0, "speed": 0, "defense": 2},
    "chainmail": {"name": "⛓️ زره زنجیری", "type": "armor", "price": 2000, "power": 0, "speed": 0, "defense": 3},
    "iron_armor": {"name": "🪨 زره آهنی", "type": "armor", "price": 3500, "power": 0, "speed": 0, "defense": 4},
    "steel_armor": {"name": "🔩 زره فولادی", "type": "armor", "price": 5000, "power": 0, "speed": 0, "defense": 5},
    "bronze_armor": {"name": "🟡 زره برنزی", "type": "armor", "price": 10000, "power": 0, "speed": 0, "defense": 7},
    "golden_armor": {"name": "🟠 زره طلایی", "type": "armor", "price": 15000, "power": 0, "speed": 0, "defense": 9},
    "dragon_scale": {"name": "🐉 پولک اژدها", "type": "armor", "price": 20000, "power": 0, "speed": 0, "defense": 11},
    "shadow_armor": {"name": "🌑 زره سایه", "type": "armor", "price": 30000, "power": 0, "speed": 0, "defense": 13},
    "phoenix_armor": {"name": "🔥 زره ققنوس", "type": "armor", "price": 50000, "power": 0, "speed": 0, "defense": 16},
    "titan_armor": {"name": "⛰️ زره تیتان", "type": "armor", "price": 65000, "power": 0, "speed": 0, "defense": 19},
    "thunder_armor": {"name": "⚡ زره رعد", "type": "armor", "price": 80000, "power": 0, "speed": 0, "defense": 22},
    "holy_armor": {"name": "✨ زره مقدس", "type": "armor", "price": 100000, "power": 0, "speed": 0, "defense": 25},
    "eternal_armor": {"name": "♾️ زره جاویدان", "type": "armor", "price": 150000, "power": 0, "speed": 0, "defense": 30},
    "celestial_armor": {"name": "🌌 زره آسمانی", "type": "armor", "price": 200000, "power": 0, "speed": 0, "defense": 35},
    
    # ===== اسب‌ها (۵ عدد) =====
    "pony": {"name": "🐴 کره اسب", "type": "horse", "price": 10000, "power": 2, "speed": 2, "defense": 0},
    "war_horse": {"name": "🐎 اسب جنگی", "type": "horse", "price": 30000, "power": 5, "speed": 5, "defense": 0},
    "nightmare": {"name": "🌙 کابوس", "type": "horse", "price": 80000, "power": 9, "speed": 8, "defense": 0},
    "pegasus": {"name": "🦄 پگاسوس", "type": "horse", "price": 150000, "power": 14, "speed": 12, "defense": 0},
    "celestial_horse": {"name": "🌠 اسب آسمانی", "type": "horse", "price": 300000, "power": 20, "speed": 18, "defense": 0},
}

# ============================================
# ۵. کوئست‌ها
# ============================================

QUESTS = [
    {"name": "جنگجو", "desc": "۲ بار در جنگ پیروز شو", "type": "win_fight", "target": 2},
    {"name": "سرباز حرفه‌ای", "desc": "۳ بار در جنگ پیروز شو", "type": "win_fight", "target": 3},
    {"name": "قاتل", "desc": "۵ بار در جنگ پیروز شو", "type": "win_fight", "target": 5},
    {"name": "حمله‌کننده", "desc": "۱ بار حمله کن", "type": "attack", "target": 1},
    {"name": "غارتگر", "desc": "۲ بار حمله کن", "type": "attack", "target": 2},
    {"name": "بازرگان", "desc": "۱ آیتم بخر", "type": "buy", "target": 1},
]
