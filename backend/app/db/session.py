from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings
@lru_cache
def get_engine():
    url=get_settings().database_url
    if not url: raise RuntimeError('DATABASE_URL is required for PostgreSQL persistence')
    return create_engine(url,pool_pre_ping=True)
def dispose_engine():
    if get_engine.cache_info().currsize:
        get_engine().dispose()
        get_engine.cache_clear()
SessionLocal=sessionmaker(autocommit=False,autoflush=False)
def get_db():
    db=SessionLocal(bind=get_engine())
    try: yield db
    finally: db.close()
def database_is_ready() -> bool:
    try:
        engine=get_engine()
        with engine.connect() as conn: conn.exec_driver_sql("SELECT 1")
        return True
    except Exception: return False
