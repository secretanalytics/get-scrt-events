
from sqlalchemy import func
from sqlalchemy.orm import Session

from db import parse_block
import models, schemas


def get_db_tip(db: Session, chain_id):
    max_height = db.query(func.max(models.Block.height)).filter(models.Block.chain_id == chain_id).scalar()
    return max_height

def create_blocks(db:Session, blocks, chain_id):
    for i in blocks:    
        block_in = parse_block(i, chain_id)
        db.add(block_in)
    db.commit()


