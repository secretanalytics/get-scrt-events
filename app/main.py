import os
import json
import time
import asyncio
import logging
from typing import List

from sqlalchemy.orm import Session

import crud, models, schemas
from db import SessionLocal, engine
from node import Node

models.Base.metadata.create_all(bind=engine)

async def run():
    remote_node = Node(os.environ['REMOTE_NODE'])
    chain_id = os.environ['CHAIN_ID']
    db = SessionLocal()
    while True:
        db_tip = crud.get_db_tip(db, chain_id) + 1
        chain_tip = (await remote_node.get_chaintip())['chaintip']
        if db_tip < chain_tip:
            await remote_node.iter_blocks(db_tip, chain_tip, db, chain_id)
        else:
            time.sleep(1)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(run())
    loop.run_forever()