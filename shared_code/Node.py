import aiohttp
import logging

class Node:

    def __init__(self, remote):
        self.remote = "{}:26657".format(remote)

    async def get_status(self):
        logging.debug("Getting status for {}".format(self.remote))
        path = "{}/status?".format(self.remote)
        out = await self.__get_path(path)
        logging.info("Got status for {}".format(self.remote))
        return out

    async def get_netinfo(self):
        logging.debug("Getting net info for {}".format(self.remote))
        path = "{}/net_info?".format(self.remote)
        out = await self.__get_path(path)
        logging.info("Got net info for {}".format(self.remote))
        return out

    async def __get_path(self, path):
        try:
            logging.debug("Attempting HTTP get to path {}".format(path))
            async with aiohttp.ClientSession() as session:
                async with session.get(path) as resp:
                    logging.info("Successful HTTP get to path {}".format(path))
                    return resp.json()
        except Exception as e:
            logging.error("Failed get to path {} with error - {}".format(path, e))