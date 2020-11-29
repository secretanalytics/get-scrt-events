import aiohttp
import logging


async def get_path(path):
    try:
        logging.debug("Attempting HTTP get to path {}".format(path))
        async with aiohttp.ClientSession() as session:
            async with session.get(path) as resp:
                logging.info("Successful HTTP get to path {}".format(path))
                return resp.json()
    except Exception as e:
        logging.error("Failed get to path {} with error - {}".format(path, e))
            
