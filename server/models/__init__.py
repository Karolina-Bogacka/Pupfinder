from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost/pupfinder"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={})
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()


def get_db():
    try:
        yield db
    finally:
        db.close()
