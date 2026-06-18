# database/schema.py
# ============================================
# مدل‌های دیتابیس (همه جدول‌ها)
# ============================================

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from config import Config

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String(20), unique=True, index=True)
    username = Column(String(15), unique=True)
    
    # کلاس و سطح
    class_name = Column(String(20))  # warrior, archer, defender, assassin
    level = Column(Integer, default=1)
    title = Column(String(30), default="کهنه‌سرباز")
    exp = Column(Integer, default=0)
    exp_needed = Column(Integer, default=100)
    
    # منابع
    gold = Column(Integer, default=100)
    
    # آمار
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    
    # ارتش
    army = Column(String(20), nullable=True)  # byzantine, holy_roman, persian, mongol
    army_join_time = Column(DateTime, nullable=True)
    
    # ارتش شخصی (لول ۱۵+)
    has_personal_army = Column(Boolean, default=False)
    personal_army_name = Column(String(30), nullable=True)
    personal_army_power = Column(Integer, default=0)
    soldiers_count = Column(Integer, default=0)
    
    # قلمرو
    territories = relationship("Territory", back_populates="owner")
    
    # کلن
    clan_id = Column(Integer, ForeignKey("clans.id"), nullable=True)
    clan = relationship("Clan", back_populates="members")
    clan_join_date = Column(DateTime, nullable=True)
    
    # اینونتوری (رابطه)
    inventory = relationship("Inventory", back_populates="user")
    
    # تجهیزات فعلی
    current_weapon = Column(String(30), nullable=True)
    current_armor = Column(String(30), nullable=True)
    current_horse = Column(String(30), nullable=True)
    
    # کول‌داون‌ها
    last_fight = Column(DateTime, nullable=True)
    fight_blocked_until = Column(DateTime, nullable=True)
    last_attack = Column(DateTime, nullable=True)
    last_territory_collect = Column(DateTime, nullable=True)
    
    # کوئست‌های روزانه (ذخیره به صورت JSON)
    daily_quests = Column(Text, default="[]")
    last_daily = Column(DateTime, nullable=True)
    
    # تاریخچه
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_key = Column(String(30))  # کلید آیتم
    equipped = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="inventory")


class Territory(Base):
    __tablename__ = "territories"
    
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(30))
    level = Column(String(20))  # small, medium, large
    gold_per_hour = Column(Integer)
    last_collected = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="territories")


class Clan(Base):
    __tablename__ = "clans"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)
    leader_id = Column(Integer, ForeignKey("users.id"))
    level = Column(Integer, default=1)
    total_power = Column(Integer, default=0)
    member_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    leader = relationship("User", foreign_keys=[leader_id])
    members = relationship("User", back_populates="clan", foreign_keys="User.clan_id")


class Duel(Base):
    __tablename__ = "duels"
    
    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    joiner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    bet_amount = Column(Integer)
    status = Column(String(20), default="waiting")  # waiting, started, finished
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    
    creator = relationship("User", foreign_keys=[creator_id])
    joiner = relationship("User", foreign_keys=[joiner_id])
    winner = relationship("User", foreign_keys=[winner_id])


# ============================================
# تابع ایجاد جداول
# ============================================

def init_db():
    engine = create_engine(Config.DATABASE_URL)
    Base.metadata.create_all(engine)
    return engine
