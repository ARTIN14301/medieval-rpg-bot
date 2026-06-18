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
        "bonus": {"power": 20, "gold": 0, "escape": 0, "defense": 0}
    },
    "archer": {
        "name": "کماندار",
        "emoji": "🏹",
        "bonus": {"power": 15, "gold": 0, "escape": 10, "defense": 0}
    },
    "defender": {
        "name": "مدافع",
        "emoji": "🛡️",
        "bonus": {"power": 0, "gold": 0, "escape": 0, "defense": 20}
    },
    "assassin": {
        "name": "آسـاسین",
        "emoji": "🗡️",
        "bonus": {"power": 5, "gold": 15, "escape": 0, "defense": 0}
    }
}

# ============================================
# ۲. ارتش‌های دیفالت
# ============================================

ARMIES = {
    "byzantine": {
        "name": "امپراتوری بیزانس",
        "emoji": "🛡️",
        "bonus": 8
    },
    "holy_roman": {
        "name": "امپراتوری مقدس روم",
        "emoji": "⚔️",
        "bonus": 7
    },
    "persian": {
        "name": "شاهنشاهی ایران",
        "emoji": "🦁",
        "bonus": 5
    },
    "mongol": {
        "name": "ایلخانان مغول",
        "emoji": "🏹",
        "bonus": 10
    }
}

# ============================================
# ۳. لقب‌ها (هر ۲ لول - ۵۰ لقب)
# ============================================

TITLES = {
    1: "کهنه‌سرباز",
    3: "دلاور",
    5: "پهلوان",
    7: "شمشیرزن ماهر",
    9: "سردار جنگ",
    11: "فاتح روستاها",
    13: "نجیب‌زاده",
    15: "فرمانده",  # 🔥 شروع بازی اصلی
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
    """دریافت لقب بر اساس لول"""
    if level < 1:
        return TITLES[1]
    if level > 99:
        return TITLES[99]
    # پیدا کردن نزدیک‌ترین لول فرد پایین‌تر
    closest = level if level % 2 == 1 else level - 1
    if closest < 1:
        closest = 1
    return TITLES.get(closest, TITLES[1])

# ============================================
# ۴. آیتم‌های شاپ
# ============================================

ITEMS = {
    # ===== سلاح‌ها =====
    "dagger": {"name": "خنجر کهنه", "type": "weapon", "price": 1000, "effect": 2},
    "short_sword": {"name": "شمشیر کوتاه", "type": "weapon", "price": 2000, "effect": 3},
    "iron_sword": {"name": "شمشیر آهنی", "type": "weapon", "price": 3500, "effect": 4},
    "steel_sword": {"name": "شمشیر فولادی", "type": "weapon", "price": 5000, "effect": 5},
    "crimson_blade": {"name": "تیغ زرشکی", "type": "weapon", "price": 10000, "effect": 7},
    "shadow_fang": {"name": "نیش سایه", "type": "weapon", "price": 15000, "effect": 9},
    "dragon_claw": {"name": "چنگال اژدها", "type": "weapon", "price": 20000, "effect": 11},
    "thunder_bringer": {"name": "آورنده رعد", "type": "weapon", "price": 30000, "effect": 13},
    "frost_mourne": {"name": "سوگ یخبندان", "type": "weapon", "price": 50000, "effect": 16},
    "hell_fire": {"name": "آتش دوزخی", "type": "weapon", "price": 65000, "effect": 19},
    "star_breaker": {"name": "ستاره‌شکن", "type": "weapon", "price": 80000, "effect": 22},
    "void_edge": {"name": "لبه خلأ", "type": "weapon", "price": 100000, "effect": 25},
    "soul_reaper": {"name": "دروگر ارواح", "type": "weapon", "price": 150000, "effect": 30},
    "god_slayer": {"name": "خداکش", "type": "weapon", "price": 200000, "effect": 35},
    "world_ender": {"name": "پایان جهان", "type": "weapon", "price": 300000, "effect": 40},
    "apocalypse": {"name": "آخرالزمان", "type": "weapon", "price": 500000, "effect": 46},
    "eternity": {"name": "جاودانگی", "type": "weapon", "price": 700000, "effect": 52},
    "primordial": {"name": "نخستین", "type": "weapon", "price": 850000, "effect": 58},
    "infinity": {"name": "بی‌نهایت", "type": "weapon", "price": 1000000, "effect": 65},
    
    # ===== زره‌ها =====
    "leather_armor": {"name": "زره چرمی", "type": "armor", "price": 1000, "effect": 2},
    "studded_armor": {"name": "زره میخی", "type": "armor", "price": 2000, "effect": 3},
    "chainmail": {"name": "زره زنجیری", "type": "armor", "price": 3500, "effect": 4},
    "iron_armor": {"name": "زره آهنی", "type": "armor", "price": 5000, "effect": 5},
    "steel_armor": {"name": "زره فولادی", "type": "armor", "price": 10000, "effect": 7},
    "golden_armor": {"name": "زره طلایی", "type": "armor", "price": 15000, "effect": 9},
    "dragon_scale": {"name": "پولک اژدها", "type": "armor", "price": 20000, "effect": 11},
    "dark_armor": {"name": "زره تاریکی", "type": "armor", "price": 30000, "effect": 13},
    "phoenix_armor": {"name": "زره ققنوس", "type": "armor", "price": 50000, "effect": 16},
    "titan_armor": {"name": "زره تیتان", "type": "armor", "price": 65000, "effect": 19},
    "thunder_armor": {"name": "زره رعد", "type": "armor", "price": 80000, "effect": 22},
    "holy_armor": {"name": "زره مقدس", "type": "armor", "price": 100000, "effect": 25},
    "eternal_armor": {"name": "زره جاویدان", "type": "armor", "price": 150000, "effect": 30},
    "god_armor": {"name": "زره خدایان", "type": "armor", "price": 200000, "effect": 35},
    "celestial_armor": {"name": "زره آسمانی", "type": "armor", "price": 300000, "effect": 40},
    "immortal": {"name": "جاودانگی", "type": "armor", "price": 500000, "effect": 46},
    "void_armor": {"name": "زره خلأ", "type": "armor", "price": 700000, "effect": 52},
    "creation": {"name": "آفرینش", "type": "armor", "price": 850000, "effect": 58},
    "absolute": {"name": "مطلق", "type": "armor", "price": 1000000, "effect": 65},
    
    # ===== اسب‌ها =====
    "pony": {"name": "کره اسب", "type": "horse", "price": 10000, "effect": 5},
    "war_horse": {"name": "اسب جنگی", "type": "horse", "price": 30000, "effect": 10},
    "nightmare": {"name": "کابوس", "type": "horse", "price": 80000, "effect": 18},
    "pegasus": {"name": "پگاسوس", "type": "horse", "price": 150000, "effect": 28},
    "shadow_stallion": {"name": "اسب نریان سایه", "type": "horse", "price": 300000, "effect": 40},
    "celestial_horse": {"name": "اسب آسمانی", "type": "horse", "price": 500000, "effect": 55},
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
