import os
import datetime
import time

import pytz

from binance_ import Listing as BinanceListing
from common.listing import AbstractListing

# Set the timezone to Kiev
timezone = pytz.timezone('Europe/Kiev')

BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')

listing: AbstractListing = BinanceListing(BINANCE_API_KEY, BINANCE_API_SECRET)

READY = True

# Перед запуском: 
# 1. налаштуй проксі для API ключів.
# 2. простав час для старту.
# 3. протестуй на будь-якій іншій монеті.
# 4. зміни symbol на необхідну тобі пару.

def execute_listing_money_making(target_date: datetime.datetime, symbol: str='ETHUSDT', count_of_usdt: int=10):
    bought = False
    sold = False
    while not (bought and sold):
        current_time = datetime.datetime.now(timezone)
        print(f'Current time: {current_time.hour}:{current_time.minute}:{current_time.second}')

        # Check if the current time matches the target date and time
        if current_time >= target_date and current_time.hour == target_date.hour and current_time.minute == target_date.minute and not bought:
            print("BUY")
            listing.buy(symbol, count_of_usdt)
            bought = True

        if current_time >= target_date and current_time.hour == target_date.hour and current_time.minute == target_date.minute and (current_time.second > 11 and current_time.second < 20) and not sold:
            print("SELL")
            listing.sell(symbol)
            sold = True

        time.sleep(1)

# Set the target date and time
target_date = datetime.datetime(year=2024, month=3, day=11, hour=2, minute=31, second=0, tzinfo=timezone)

if READY:
    print('-'*10, 'Started', '-'*10)
    execute_listing_money_making(target_date, symbol='BTCUSDT', count_of_usdt=8)

