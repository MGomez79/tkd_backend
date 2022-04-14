from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

engine = create_engine("postgresql://miguel:angel@localhost:5432/taekwondo2")

Session = sessionmaker(bind=engine)
