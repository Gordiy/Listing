import time

from binance.spot import Spot


class Listing:
    """Class to buy and sell pairs on listing."""
    def __init__(self, api_key: str, api_secret: str) -> None:
        self.client = Spot(api_key=api_key, api_secret=api_secret)
        self._quantity = 1

    def buy(self, symbol: str, count_of_usdt: int) -> None:
        self._get_quantity(symbol, count_of_usdt)
        self._trade(symbol, 'BUY')

    def sell(self, symbol: str) -> None:
        self._trade(symbol, 'SELL')

    def _trade(self, symbol: str, side: str='BUY') -> None:
        params = self._get_params(symbol, side)

        try:
            time.sleep(0.5)

            response = self.client.new_order(**params)
            print(response)
        except Exception as e:
            print("Error", e.args)

    def _get_params(self, symbol: str, side: str) -> dict:
        """
        Get request params.
        
        :param symbol: ETHUSDT
        :param side: BUY or SELL
        """
        return {
            'symbol': symbol,
            'side': side,
            'type': 'LIMIT',
            'timeInForce': 'GTC',
            'quantity': self._quantity,
            'price': self._get_price(symbol)
        }

    def _get_quantity(self, symbol: str, count_of_usdt: float) -> str:
        """Get quantity of order."""
        limit_zone = self._get_limit_zone(symbol)
        quantity = count_of_usdt / self._get_price(symbol)
        precision = self.__get_precision(limit_zone[2])

        self._quantity = round(quantity, precision)

        if self._quantity < limit_zone[0]:
            self._quantity = limit_zone[0]

        if self._quantity > limit_zone[1]:
            self._quantity = limit_zone[1]

        return self._quantity

    def _get_price(self, symbol: str) -> float:
        """Get ticker price."""
        price_val = self.client.ticker_price(symbol=symbol)

        price = float(price_val['price'])
        return price
    
    def _get_limit_zone(self, symbol: str) -> tuple:
        """Get limit zone."""
        exchange_info = self.client.exchange_info()
        for symbol_info in exchange_info['symbols']:
            if symbol_info['symbol'] == symbol:
                for filter_info in symbol_info['filters']:
                    if filter_info['filterType'] == 'LOT_SIZE':
                        min_qty = float(filter_info['minQty'])
                        max_qty = float(filter_info['maxQty'])
                        step_size = float(filter_info['stepSize'])
                        print(f"Lot size for {symbol}: Min Qty: {min_qty}, Max Qty: {max_qty}, Step Size: {step_size}")
                        return (min_qty, max_qty, step_size)
                    
        return (0, 1000000, 0.01)
                    
    def __get_precision(self, num: float):
        number_str = str(num)
        max_precision = 4

        if 'e' in number_str: return int(number_str[-1]) if int(number_str[-1]) <= max_precision else max_precision

        precision = number_str[::-1].find('.')

        return precision if precision <= max_precision else max_precision