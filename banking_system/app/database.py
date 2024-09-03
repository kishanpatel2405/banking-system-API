from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = 'postgresql://bank_user:123@localhost/banking_system'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
