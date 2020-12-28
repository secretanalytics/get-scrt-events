from typing import List, Optional
from pydantic import BaseModel


class Attribute(BaseModel):
    id: int
    a_key: str
    a_value: str
    event_id: int

    class Config:
        orm_mode = True

class Event(BaseModel):
    id: int
    e_type: str
    tx_id: Optional[int]
    block_id: str
    attributes: List[Attribute]

    class Config:
        orm_mode = True

class Transaction(BaseModel):
    id: int
    gas_wanted: int
    gas_used: int
    success: bool
    log: str
    block_id: str
    events: List[Event]

    class Config:
        orm_mode = True

class Block(BaseModel):
    id: str
    height: int
    chain_id: str
    events: List[Event]
    transactions: Optional[List[Transaction]]

    class Config:
        orm_mode = True
    
