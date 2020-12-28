import logging
from sqlalchemy import func
from sqlalchemy.orm import Session

from db import parse_block
import models, schemas


def get_db_tip(db: Session, chain_id):
    max_height = db.query(func.max(models.Block.height)).filter(models.Block.chain_id == chain_id).scalar()
    return max_height

def create_block(db:Session, block, chain_id):  
    block_in = parse_block(block, chain_id)
    try:
        db.add(block_in)
        db.commit()
    except Exception as e:
        logging.error("{}".format(e))


