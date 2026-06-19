# database/db.py
# ============================================
# مدیریت اتصال به دیتابیس
# ============================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from database.schema import Base,

# ایجاد engine
engine = create_engine(Config.DATABASE_URL)

# ایجاد session
SessionLocal = sessionmaker(bind=engine)

def get_session():
    """دریافت یک session جدید"""
    return SessionLocal()

def init_database():
    Base.metadata.create_all(engine)
    print("✅ دیتابیس با موفقیت ساخته شد!")
