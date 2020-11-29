import logging
import asyncio

from ..shared_code.Node import Node

async def main(node, msg: func.Out[str]):
    logging.debug("Getting {} chaintip".format(node))
    path = "{}:26657/status?".format(node)
    out = await get_path(path)
    msg.set(out)
    return out
