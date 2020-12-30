# Parsing Explanation

When the block_results endpoint is queried, a json response is returned which contains the information about that specific block. 

For example, if `block_results?height=520158` were to be queried, [this](data/example.json) would be returned. 

To make this information useful, and able to be inserted into postgres we must first parse it. 

In the database, each block is stored in the `blocks` table as a `Block` object:

```python
class Block(Base):
    __tablename__ = 'blocks'
    id = Column(String, primary_key=True)
    height = Column('height', Integer)
    chain_id = Column('chain_id', String)
    events = relationship("Event")
    transactions = relationship("Transaction")
```

The primary key for a block(`id`) is the `height` and `chain_id` concatenated into a string. Each block has a relation with a list of events and transactions. 

A transaction object is identified by an autoincremented integer `id`. 

```python
class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    gas_wanted = Column('gas_wanted', Integer)
    gas_used = Column('gas_used', Integer)
    success = Column('success', Boolean)
    log = Column('log', String)
    block_id = Column('block_id', String, ForeignKey('blocks.id'))
    events = relationship("Event")
```

The `gas_wanted`, `gas_used`, `success`, `block_id` and `log` are stored for all transactions. If a transaction has failed (denoted by a `success = False`), there would be no related events to decode. 