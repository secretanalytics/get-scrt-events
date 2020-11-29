import logging
import asyncio
import azure.functions as func

from shared_code.Node import Node

async def main(node, msg: func.Out[str]):
    try:
        logging.debug("Getting {} status".format(node.remote))
        out = await node.get_netinfo()
    except Exception as e:
        logging.error("Failed getting status {}".format(e))
    msg.set(out)