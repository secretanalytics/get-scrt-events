import unittest
import asyncio

import azure.functions as func

from HttpTrigger import main

class TestFunction(unittest.IsolatedAsyncioTestCase):
    async def test_http_trigger(self):

        req = func.HttpRequest(
            method='GET',
            body=None,
            url="/api/orchestrators/DurableOrchestration",
            params={'test':'pass'}

        )
        starter = 'Test'
        resp = await main(req, starter)
        