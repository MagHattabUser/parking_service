from sqlalchemy import create_engine
from domain.models import Base


DATABASE_URL = "postgresql+asyncpg://postgres:admin@db:5432/parking"

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)
