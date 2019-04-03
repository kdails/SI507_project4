from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
from sqlalchemy.sql import select
import json, csv
# some of this code based on info from https://docs.sqlalchemy.org/en/latest/orm/collections.html ( specifically many to many relationships for stateparks with the same names)
# set up base, session, and engine
engine = create_engine('sqlite:///state_parks_info.sqlite', echo=False)

Base = declarative_base()

session = scoped_session(sessionmaker())


Base.metadata.bind = engine
session.configure(bind=engine)

# define db function making
def init_db():
    Base.metadata.create_all(engine)
    return engine

# define table class
class State(Base):
    __tablename__ = 'States'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    State = Column(String(24), nullable = False)
    Abbr = Column(String(2), nullable = False)
    URL = Column(String(250), nullable = False)
    Parks_Rel = relationship('Park',secondary='association',back_populates='State_Rel',lazy='dynamic')
# define table class
class Park(Base):
    __tablename__ = 'Parks'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(250))
    Type = Column(String(250))
    Descr = Column(String(2000))
    Location = Column(String(250))
    State_Rel = relationship('State',secondary='association',back_populates='Parks_Rel',lazy='dynamic')
# define table class
class StateParkAssociation(Base):
    __tablename__ = 'association'
    State_Id = Column(Integer, ForeignKey('States.Id'),primary_key=True)
    Park_Id = Column(Integer, ForeignKey('Parks.Id'),primary_key=True)
    State_Assoc = relationship(State, backref=backref('Parks_Assoc'))
    Park_Assoc = relationship(Park, backref=backref('State_Assoc'))

init_db()
