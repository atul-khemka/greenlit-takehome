from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# connection url will not be directly used in code in production
SQLALCHEMY_DATABASE_URL = "postgresql://wqzatntq:mueneA9FretV8WAd6YAr_CKkIQCobZcE@rain.db.elephantsql.com/wqzatntq"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
