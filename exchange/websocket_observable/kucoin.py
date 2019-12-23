import asyncio
import json
import logging
import random
import time
from enum import Enum

import aiohttp
import websockets

from common.order_book import KuCoinOrderBook
from exchange.websocket_observable._base import BaseWsObservable

logger = logging.getLogger("django")


class MatchEngineEventType(Enum):
    RECEIVED = "received"
    OPEN = "open"
    DONE = "done"
    CHANGE = "change"
    MATCH = "match"


class KuCoinWebsocketObservable(BaseWsObservable):

    def __init__(self):
        super().__init__()

        self.order_book = None
        self.symbol_str = None

        self.replay_task = None
        self.server = None

        self.q = asyncio.Queue()

        self._first_incremental_seq_checked = False
        self._last_incremental_seq = None

    def set_symbol(self, symbol_str):
        self.symbol_str = symbol_str

    async def initialize(self):
        pass

    async def get_url(self):
        pass

    async def prepare_conn(self):

        logger.info("正在获取 Websocket 服务器地址...")

        url = "https://api.kucoin.com/api/v1/bullet-public"
        async with aiohttp.ClientSession() as session:
            async with session.post(url) as resp:

                resp_json = await resp.json()

                if resp_json.get("code") == "200000":
                    data = resp_json.get("data")

                    token = data.get("token")

                    servers = data.get("instanceServers", [])

                    num_servers = len(servers)

                    if num_servers:
                        logger.info("共返回{}个可用WS服务器".format(num_servers))

                        _server = random.choice(servers)

                        logger.info("随机选择了{}.".format(_server))

                        _server["token"] = token

                        return _server
                else:
                    logger.error("获取WS服务器的请求失败: {}".format(resp_json))

    async def initialize_order_book_snapshot(self, symbol_str=None):

        url = "https://openapi-v2.kucoin.com/api/v1/market/orderbook/level3?symbol={}".format(symbol_str if symbol_str
                                                                                              else self.symbol_str)

        await asyncio.sleep(1)  # todo 删除之 (暂时加上，让WS消息缓存1s后 再请求snapshot)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp_json = await resp.json()

                logger.debug("got order book snapshot: {}".format(resp_json))

                _order_book_asks = resp_json["data"]["asks"]
                _order_book_bids = resp_json["data"]["bids"]
                _order_book_snapshot_sequence = int(resp_json["data"]["sequence"])
                _order_book_snapshot_time = resp_json["data"]["time"]

                self.order_book = KuCoinOrderBook(_order_book_asks, _order_book_bids, _order_book_snapshot_sequence,
                                                  _order_book_snapshot_time)

    async def connect(self):

        self.server = await self.prepare_conn()

        endpoint = self.server["endpoint"]
        token = self.server["token"]

        uri = "{}?token={}&connectId={}".format(endpoint, token, str(int(time.time() * 1000)))

        try:
            logger.info("creating websocket connection, uri: {}.".format(uri))

            self.ws_conn = await asyncio.wait_for(websockets.connect(uri, ssl=self.server["encrypt"]), timeout=10)

        except asyncio.TimeoutError as e:

            logger.error("timeout creating websocket connection")
            raise e

        except Exception as e:
            logger.error("error while creating websocket connection: {}.".format(e))
            raise e
        else:
            logger.info("created websocket connection, uri: {}.".format(uri))
            self._is_ws_connected = True

    async def on_err(self):

        logger.info("on error, will reconnect...")

        self._is_ws_connected = False

        if self.ws_conn is not None and not self.ws_conn.closed:
            await self.ws_conn.close()

        self._first_incremental_seq_checked = False
        self._last_incremental_seq = None
        self.order_book = None

        self.replay_task.cancel()

        self.q = asyncio.Queue()  # 重置 q

    async def _do_update(self, _data):
        logger.debug("doing update...")

        _type = _data["type"]
        _sequence = int(_data["sequence"])

        if _sequence <= self.order_book.snapshot_seq:
            logger.info("增量Seq 小于 Snapshot Seq， 跳过 ({} < {})".format(_sequence, self.order_book.snapshot_seq))
            return

        logger.debug("========= 应该replay，消息类型: {}".format(_type))

        if _type == MatchEngineEventType.RECEIVED.value:
            logger.debug("跳过")
        elif _type == MatchEngineEventType.OPEN.value:
            logger.debug("添加Order")
            self.order_book.add_order(_data)
        elif _type == MatchEngineEventType.DONE.value:
            _side = _data["side"]
            _order_id = _data["orderId"]
            logger.debug("移除 {} 方，order id 为 {} 的 Order.".format(_side, _order_id))
            self.order_book.remove_order(_data)
        elif _type == MatchEngineEventType.CHANGE.value:
            _side = _data["side"]
            _order_id = _data["orderId"]
            _new_size = _data["newSize"]
            logger.debug("修改数量 {} {} 为 {}".format(_side, _order_id, _new_size))
            self.order_book.change_order(_data)
        elif _type == MatchEngineEventType.MATCH.value:
            logger.debug("订单 部分被吃")
            self.order_book.match_order(_data)
        else:
            logger.error("error 未处理的撮合引擎 消息类型 {}".format(_data))
            # self.on_err()

        # await self.on_order_book()

    async def handle_ws_resp(self, msg):

        try:
            json_message = json.loads(msg)
        except Exception as e:
            logger.error("on_data error: {} | raw_message: {}".format(e, msg))
        else:

            logger.info("got ws response: {}.".format(json_message))

            if json_message.get("type") == "welcome":

                logger.info("handshake done...")

                logger.info("subscribing order_book channel.")

                depth_subscribe_msg = {
                    "id": 1545910660742,
                    "type": "subscribe",
                    "topic": "/market/level3:{}".format(self.symbol_str),
                    "privateChannel": False,
                    "response": True
                }

                await self.ws_conn.send(json.dumps(depth_subscribe_msg))

            elif json_message.get("type") == "message" and json_message.get("topic") and json_message.get(
                    "topic").startswith("/market/level3"):

                await self.on_order(json_message["data"])

                # await self.q.put(json_message)

    async def start_fetch_order_book(self):
        try:
            async for msg in self.ws_conn:
                await self.handle_ws_resp(msg)
        except Exception as e:
            logger.error("error fetching order_book: {}.".format(e))
            await self.on_err()
        finally:
            await self.ws_conn.close()

    async def on_order(self, o):
        for observer in self.observers:
            await observer.on_order(o)
