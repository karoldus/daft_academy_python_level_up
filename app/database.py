import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://jevmwadvvvfcze:50a5227667827a3211b3338f6ba02d429234a380cbf9b37431fbbe9db1a7a68b@ec2-54-228-9-90.eu-west-1.compute.amazonaws.com:5432/d8gk62d1rk0ujs"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
