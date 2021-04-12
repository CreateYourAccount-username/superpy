class buy_item():
    def __init__(self, id_num, product_name, buy_date, buy_price,
                 expiration_date):
        self.id_num = id_num
        self.product_name = product_name
        self.buy_date = buy_date
        self.buy_price = buy_price
        # you can still sell on date but not after
        self.expiration_date = expiration_date


class sell_item():
    def __init__(self, id_num, bought_id, sell_date, sell_price):
        self.id_num = id_num
        self.bought_id = bought_id
        self.sell_date = sell_date
        self.sell_price = sell_price
