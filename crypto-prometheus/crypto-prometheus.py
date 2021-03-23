#!/usr/bin/env python3
'''
Example -a/--address options:
-a btc 1234
-a eth 0x1234
-a coinbase_pro btc:key:passphrase:secret
-a coinbase_pro eth:key:passphrase:secret
'''

from optparse import OptionParser
from lib.eth import Eth
from lib.btc import Btc
from lib.coinbase_pro import CoinbasePro

import datetime
import logging
import os
import sys
import time

from prometheus_client import start_http_server, Gauge

logging.basicConfig(stream=sys.stdout, level=getattr(logging, os.getenv('LOG_LEVEL', 'WARN')))

parser = OptionParser()
parser.add_option("-a", "--address", dest="addresses",
                  action="append", nargs=2, default=[],
                  metavar="currency address")
parser.add_option("-p", "--prometheus-server-port",
                  default=8000,
                  help="Prometheus server port (default: 8000)")
parser.add_option("-i", "--update-interval",
                  default=10,
                  help="Update interval in seconds (default: 10)")
(options, args) = parser.parse_args()

print("options: %s" % options)

if os.getenv('CRYPTO_PROMETHEUS_ADDRESSES', ''):
  for address in os.getenv('CRYPTO_PROMETHEUS_ADDRESSES', '').split(','):
    options.addresses.append((address.strip().split(' ')[0],
                              address.strip().split(' ')[1]))

start_http_server(options.prometheus_server_port, addr='0.0.0.0')
crypto_price_gauge = Gauge('crypto_price', 'Price of Crypto', ['currency'])
crypto_wallet_balance_gauge = Gauge('crypto_wallet_balance', 'Wallet balance of Crypto', ['currency', 'wallet_address'])
crypto_value_gauge = Gauge('crypto_value', 'Value of Crypto wallet', ['currency', 'wallet_address'])
crypto_total_value_gauge = Gauge('crypto_total_value', 'Value of all Crypto wallets')
last_update_timestamp_gauge = Gauge('last_update_timestamp_s', 'UNIX timestamp in s of last update')

while True:
  total = 0
  for address in options.addresses:
    if address[0].lower() == 'eth':
      currency_processor = Eth(address[1])
    elif address[0].lower() == 'btc':
      currency_processor = Btc(address[1])
    elif address[0].lower() == 'coinbase_pro':
      currency_processor = CoinbasePro(address[1].split(':')[0],
                                       address[1].split(':')[1],
                                       address[1].split(':')[2],
                                       address[1].split(':')[3])
    else:
      currency_processor = None

    if currency_processor:
      price = currency_processor.get_current_price()
      balance = currency_processor.get_wallet_balance()
      print("[%s %s] price: %s, balance: %s, value: $%.2f" % (address[0], address[1], 
                                                              price, balance, price*balance), flush=True)
      total = total + price * balance

      crypto_price_gauge.labels(address[0]).set(price)
      crypto_wallet_balance_gauge.labels(address[0], address[1]).set(balance)
      crypto_value_gauge.labels(address[0], address[1]).set(price * balance)

  print("total: $%.2f" % total, flush=True)
  crypto_total_value_gauge.set(total)
  last_update_timestamp_gauge.set_to_current_time()
  last_update_timestamp_gauge._documentation = "Last update: %s" % (datetime.datetime.now())

  [ time.sleep(1) for x in range(options.update_interval) ]
