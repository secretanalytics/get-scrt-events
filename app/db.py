import os
import json
import base64

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

import models

engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URL'])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def parse_block(block, chain_id):
    out = {
        'chain_id':chain_id,
        'height':block['height']
        }
    out['id'] = ':'.join([out['chain_id'], str(out['height'])])
    txs = block['txs_results']
    if txs:
        out['transactions'] = parse_txs(txs, out['id'])
    events = block['begin_block_events']
    end_events = block['end_block_events']
    if end_events:
        events.extend(end_events)
    out['events'] = parse_events(events, out['id'])
    return models.Block(**out)

def parse_txs(txs, block_id):
    return [__parse_tx(i, block_id) for i in txs]

def __parse_tx(tx, block_id):
    out = {}
    out['gas_wanted'] = int(tx['gasWanted'])
    out['gas_used'] = int(tx['gasUsed'])
    out['log'] = tx['log']
    events = tx['events']
    if events:
        out['success'] = True
        out['events'] = parse_events(events, block_id)
    else:
        out['success'] = False
    return models.Transaction(**out)

def parse_events(events_list, block_id):
    out = [__parse_event(i, block_id) for i in events_list]
    return out

def __parse_event(event, block_id):
    out = {}
    out['e_type'] = event['type']
    out['attributes'] = __decode_attributes(event['attributes'])
    out['block_id'] = block_id
    return models.Event(**out)

def __decode_attribute_dict(attr_dict):
    out = {}
    try:
        out['a_key'] = str(base64.b64decode(attr_dict['key']), 'utf-8')
    except:
        out['a_key'] = 'None'
    try:
        out['a_value'] = str(base64.b64decode(attr_dict['value']), 'utf-8')
    except:
        out['a_value'] = 'None'
    return models.Attribute(**out)
    
def __decode_attributes(attributes):
    out = [__decode_attribute_dict(i) for i in attributes]
    return out

