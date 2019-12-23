class OrderBook(object):

    def __init__(self, asks=None, bids=None, snapshot_seq=None, snapshot_time=None):
        self.asks = asks if asks else []
        self.bids = bids if bids else []

        self.snapshot_seq = snapshot_seq
        self.snapshot_time = snapshot_time

    @property
    def ask1(self):
        return self.asks[0]

    @property
    def bid1(self):
        return self.bids[0]

    @property
    def spread(self):
        return (self.ask1[0] - self.bid1[0]) / ((self.ask1[0] + self.bid1[0]) / 2)


class KuCoinOrderBook(OrderBook):

    @property
    def ask1(self):
        return self.asks[0][1:]  # [order_id, price, amount]

    @property
    def bid1(self):
        return self.bids[0][1:]

    def add_order(self, data):

        """
        当接收到 price="", size="0" 的消息时，意味着这是隐藏单
        """

        _side = data["side"]

        _order_id = data["orderId"]
        _price = data["price"]
        _size = data["size"]

        if _price == "":

            print("隐藏单...")

            return

        else:

            if _side == "buy":

                _bids = [_order for _order in self.bids if float(_order[1]) > float(_price)] + [
                    [_order_id, _price, _size]] + [_order for _order in self.bids if float(_order[1]) < float(_price)]

                self.bids = _bids

            elif _side == "sell":

                _asks = [_order for _order in self.asks if float(_order[1]) < float(_price)] + [
                    [_order_id, _price, _size]] + [_order for _order in self.asks if float(_order[1]) > float(_price)]

                self.asks = _asks

            print("添加了order {} 后 {}".format(_order_id, self))

    def remove_order(self, data):

        _side = data["side"]

        _order_id = data["orderId"]

        if _side == "buy":

            _bids = [_order for _order in self.bids if _order[0] != _order_id]

            self.bids = _bids

        elif _side == "sell":

            _asks = [_order for _order in self.asks if _order[0] != _order_id]

            self.asks = _asks

        print("移除了order {}".format(_order_id))

    def change_order(self, data):
        """
        修改对应orderid对应的买单或者卖单的数量
        """
        _side = data["side"]

        _order_id = data["orderId"]
        _price = data["price"]
        _size = data["size"]

        if _side == "buy":

            _bids = [_order for _order in self.bids if _order[0] != _order_id]

            self.bids = _bids

        elif _side == "sell":

            _asks = [_order for _order in self.asks if _order[0] != _order_id]

            self.asks = _asks

    def match_order(self, data):
        """
        减少对应makerOrderId对应的订单数量
        """
        _side = data["side"]

        _order_id = data["makerOrderId"]

        if _side == "buy":

            _asks = [order for order in self.asks if order[0] == _order_id]

            print(_asks)

            if _asks:
                """
                <class 'list'>: [['5d5100f44c06876f06852656', '11388.8', '0.035']]
                """
                assert len(_asks) == 1, "多个同ID订单。。。"

                _target_order = _asks[0]

                _sub_size = data["size"]

                _new_size = float(_target_order[2]) - float(_sub_size)

                _target_order[2] = str(_new_size)

            _bids = [order for order in self.bids if order[0] == _order_id]

            assert len(_bids) == 0, "buy side match 事件，order在bids中。。。"

        elif _side == "sell":

            _bids = [order for order in self.bids if order[0] == _order_id]

            print(_bids)

            if _bids:
                """
                <class 'list'>: [['5d51008dcdaba4193e28407f', '11381.7', '0.005994']]
                """
                assert len(_bids) == 1, "多个同ID订单。。。"

                _target_order = _bids[0]

                _sub_size = data["size"]

                _new_size = float(_target_order[2]) - float(_sub_size)

                _target_order[2] = str(_new_size)

            _asks = [order for order in self.asks if order[0] == _order_id]
            assert len(_asks) == 0, "sell side match 事件，order在asks中。。。"

        else:

            raise Exception("wrong side: {}.".format(_side))
