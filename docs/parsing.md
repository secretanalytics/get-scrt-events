# Parsing Explanation

When the block_results endpoint is queried, a json response is returned which contains the information about that specific block. 

For example, if `block_results?height=520158` were to be queried, [this](data/example.json) would be returned. 

To make this information useful, and able to be inserted into postgres we must first parse it. 

In the database, each block is stored in the `blocks` table:

```python
class Block(Base):
    __tablename__ = 'blocks'
    id = Column(String, primary_key=True)
    height = Column('height', Integer)
    chain_id = Column('chain_id', String)
    events = relationship("Event")
    transactions = relationship("Transaction")
```