#!/usr/bin/env python3

from optparse import OptionParser
from lib.eth import Eth
from lib.btc import Btc

import logging
import os
import sys

logging.basicConfig(stream=sys.stdout, level=getattr(logging, os.getenv('LOG_LEVEL', 'WARN')))

parser = OptionParser()
parser.add_option("-a", "--address", dest="addresses",
                  action="append", nargs=2,
                  metavar="currency address")
(options, args) = parser.parse_args()

print("options: %s" % options)

total = 0
for address in options.addresses:
  currency_processor = { 
    "eth": Eth(address[1]),
    "btc": Btc(address[1])
  }.get(address[0].lower(), None)
  price = currency_processor.get_current_price()
  balance = currency_processor.get_wallet_balance()
  print("[%s %s] price: %s, balance: %s, value: $%.2f" % (address[0], address[1], 
                                                        price, balance, price*balance))
  total = total + price * balance

print("total: $%.2f" % total)