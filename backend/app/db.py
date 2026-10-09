from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import get_settings

settings = get_settings()

if settings.database_url.startswith('sqlite:///./'):
    db_path = (Path(__file__).resolve().parent.parent / 'agriwater.db').as_posix()
    settings.database_url = f'sqlite:///{db_path}'

connect_args = {'check_same_thread': False} if settings.database_url.startswith('sqlite') else {}
engine = create_engine(settings.database_url, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
Base = declarative_base()
