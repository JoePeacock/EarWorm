from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///sqlite.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

engine.execute("select 1").scalar()

class Posts(Base):
	__tablename__ = 'posts'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	song = Column(String)
	url = Column(String)
	date = Column(String)

	def __init__(self, name, song, url, date):
		self.name = name
		self.song = song
		self.url = url
		self.date = date

	def __repr__(self):
		return "<User('%s','%s', '%s', '%s', '%s')>" % (self.name, self.song, self.url, self.date)

Base.metadata.create_all(engine)