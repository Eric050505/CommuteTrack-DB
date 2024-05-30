from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://checker:123456@localhost:5432/cs307"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"options": "-csearch_path=Project"})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
