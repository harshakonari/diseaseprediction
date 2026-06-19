from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ==============================
# 🔥 YOUR SUPABASE DATABASE URL
# ==============================
DATABASE_URL = "postgresql+psycopg2://postgres:%40Harsha%20k12@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()