from typing import List
import json
import logging

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from db import SessionLocal, engine
from node import Node

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/chaintip/{remote}")
async def chaintip(remote: str):
    remote_node = Node(remote)
    out = await remote_node.get_chaintip()
    return out

@app.get("/peers/{remote}")
async def peers(remote: str):
    remote_node = Node(remote)
    out = await remote_node.get_peers()
    return out

@app.get("/blocks/{chain_id}/{start}/{stop}")
async def create_block(chain_id: str, start: int, stop: int, db: Session = Depends(get_db)):
    remote_node = Node("51.140.3.67")
    blocks = await remote_node.iter_blocks(start, stop)
    try:
        crud.create_blocks(db, blocks, chain_id)
        return 'Success'
    except Exception as e:
        logging.error("{} - Failed to insert blocks {} -> {} for chain {}".format(e, start, stop, chain_id))
        return 'Fail'

@app.get("/db_tip/{chain_id}")
def db_tip(chain_id: str, db: Session = Depends(get_db)):
    db_tip = crud.get_db_tip(db, chain_id)
    return db_tip