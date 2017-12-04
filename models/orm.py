# encoding: utf-8
from sqlalchemy import create_engine
from config.config import config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# _db_url = 'postgresql+psycopg2://{user}:{password}@{host}/{db}'.format(**config.db_info)
_db_url = "mysql://{user}:{password}@{host}/{db}?charset=utf8".format(**config.db_info)

#创建引擎
engine = create_engine(_db_url, echo=config.db_echo) #max_overflow=5
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

