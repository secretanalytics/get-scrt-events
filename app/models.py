from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Block(Base):
    __tablename__ = 'blocks'
    id = Column(String, primary_key=True)
    height = Column('height', Integer)
    chain_id = Column('chain_id', String)
    events = relationship("Event")
    transactions = relationship("Transaction")

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    gas_wanted = Column('gas_wanted', Integer)
    gas_used = Column('gas_used', Integer)
    success = Column('success', Boolean)
    log = Column('log', String)
    block_id = Column('block_id', String, ForeignKey('blocks.id'))
    events = relationship("Event")

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    e_type = Column('e_type', String)
    tx_id = Column('tx_id', Integer, ForeignKey('transactions.id'), nullable=True)
    block_id = Column('block_id', String, ForeignKey('blocks.id'))
    attributes = relationship("Attribute")

class Attribute(Base):
    __tablename__ = 'attributes'
    id = Column(Integer, primary_key=True)
    a_key = Column('a_key', String)
    a_value = Column('a_value', String)
    event_id = Column('event_id', Integer, ForeignKey('events.id'))



