import typing
import aiohttp
import asyncio
import logging


class Node(object):

    def __init__(self, remote: str):
        self.remote = remote

    def get_remote(self) -> str:
        return self.remote

    @staticmethod
    def to_json(obj: object) -> str:
        """ Serializes a `SerializableClass` instance
        to a JSON string.
        Parameters
        ----------
        obj: SerializableClass
            The object to serialize
        Returns
        -------
        json_str: str
            A JSON-encoding of `obj`
        """
        return str(obj.remote)

    @staticmethod
    def from_json(json_str: str) -> object:
        """ De-serializes a JSON string to a
        `SerializableClass` instance. It assumes
        that the JSON string was generated via
        `SerializableClass.to_json`
        Parameters
        ----------
        json_str: str
            The JSON-encoding of a `SerializableClass` instance
        
        Returns
        --------
        obj: SerializableClass
            A SerializableClass instance, de-serialized from `json_str`
        """
        remote = str(json_str)
        obj = Node(remote)
        return obj
    
    async def get_chaintip(self) -> dict:
        path = "/status?"
        status = await self.__get_path(path)
        try:
            chaintip = status['result']['sync_info']['latest_block_height']
            logging.info("Chaintip for {} is {}".format(self.remote, chaintip))
            out = {'remote':self.remote, 'chaintip': chaintip}
            return out
        except Exception as e:
            logging.error("{} - Failed chaintip parse for remote {}".format(e, self.remote))
            return 'Fail'

    async def get_peers(self) -> dict:
        path = "/net_info?"
        net_info = await self.__get_path(path)
        try:
            peers = net_info['result']['peers']
            logging.info("{} has {} peers".format(self.remote, len(peers)))
            out = {'remote':self.remote, 'peers': peers}
            return out
        except Exception as e:
            logging.error("{} - Failed peers parse for remote {}".format(e, self.remote))
            return 'Fail'

    async def get_block_results(self, n_height) -> dict:
        path = "/block_results?height={}".format(n_height)
        block = await self.__get_path(path)
        try:
            out = Block(block).to_dict()
            out['remote'] = self.remote
            logging.info("Parsed block {} from remote {}".format(n_height, self.remote))
            return out
        except Exception as e:
            logging.error("{} - Failed block {} parse for remote {}".format(e, n_height, self.remote))
            return 'Fail'

    async def __get_path(self, path):
        path = "http://{}:26657{}".format(self.remote, path)
        try:
            logging.debug("Attempting HTTP get to path {}".format(path))
            async with aiohttp.ClientSession() as session:
                async with session.get(path, verify_ssl=False) as resp:
                    logging.info("Successful HTTP get to path {}".format(path))
                    result = await resp.json()
                    return result
        except Exception as e:
            logging.error("Failed get to path {} - {}".format(path, e))

    async def __iter_get_chaintip(self, session):
        path = "http://{}:26657/status?".format(self.remote)
        async with session.get(path, verify_ssl=False) as resp:
            result = await resp.json()
            try:
                chaintip = result['result']['sync_info']['latest_block_height']
                logging.info("Chaintip for {} is {}".format(self.remote, chaintip))
                return int(chaintip)
            except Exception as e:
                logging.error("{} - Failed chaintip parse for remote {}".format(e, self.remote))
                return 'Fail'

    async def __iter_get_block(self, session, height):
        path = "http://{}:26657/block_results?height={}".format(self.remote, height)
        async with session.get(path, verify_ssl=False) as resp:
            result = await resp.json()
            try:
                out = result['result']
                logging.info("Parsed block result {} from remote {}".format(height, self.remote))
                return out
            except Exception as e:
                logging.error("{} - Failed block result parse for remote {}".format(e, self.remote))
                return 'Fail'

    async def iter_blocks(self, start, stop):
        async with aiohttp.ClientSession() as session:
            out = []
            for i in range(start, stop+1):
                block_i = await self.__iter_get_block(session, i)
                out.append(block_i)
            logging.info("Gathered blocks {} -> {}".format(start, stop))
            return out
