import asyncio
import logging

import websockets

logger = logging.getLogger("ws-observable")


class BaseWsObservable(object):
    ws_conn = None
    _is_ws_connected = False

    def __init__(self):
        self.observers = []

    def attach_observer(self, o):
        self.observers.append(o)

    async def initialize(self):
        raise NotImplementedError

    async def get_url(self):
        raise NotImplementedError

    async def connect(self):
        url = await self.get_url()
        try:
            logger.info("creating websocket connection, uri: {}.".format(url))

            self.ws_conn = await asyncio.wait_for(websockets.connect(url), timeout=10)

        except asyncio.TimeoutError as e:

            logger.error("timeout creating websocket connection")
            raise e

        except Exception as e:
            logger.error("error while creating websocket connection: {}.".format(e))
            raise e
        else:
            logger.info("created websocket connection, uri: {}.".format(uri))
            self._is_ws_connected = True
