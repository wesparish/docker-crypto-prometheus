try:
  from cryptobase import CryptoBase
except:
  from .cryptobase import CryptoBase

import logging
import os
import sys
from moneywagon import (get_current_price, get_address_balance)

logging.basicConfig(stream=sys.stdout, level=getattr(logging, os.getenv('LOG_LEVEL', 'WARN')))

class Btc(CryptoBase):
  def __init__(self, address):
    super(Btc, self).__init__(address)

  def get_current_price(self):
    value = None
    
    from moneywagon.services import Bittrex
    client = Bittrex()

    try_count = 0
    while True:
      try:
        value = client.get_current_price('btc', 'usd')
        break
      except Exception as ex:
        print("Caught exception in get_current_price: %s" % ex)
        try_count += 1
        if try_count > 5:
          raise
    return value

  def get_wallet_balance(self):
    value = None
    
    from moneywagon.services import BlockChainInfo
    client = BlockChainInfo()

    try_count = 0
    while True:
      try:
        value = client.get_balance('btc', self._address)
        break
      except Exception as ex:
        print("Caught exception in get_wallet_balance: %s" % ex)
        try_count += 1
        if try_count > 5:
          raise
    return value

if __name__ == "__main__":
  import os
  print("Testing %s" % (os.path.basename(__file__)))

  import unittest
  class TestBtc(unittest.TestCase):
    def setUp(self):
      address = "35hK24tcLEWcgNA4JxpvbkNkoAcDGqQPsP"
      self.btc = Btc(address)

    def tearDown(self):
      pass

    def test_get_price_from_api(self):
      current_price = self.btc.get_current_price()
      print("current_price (btc): %s" % current_price)
      assert current_price > 0

    def test_get_wallet_balance(self):
      wallet_balance = self.btc.get_wallet_balance()
      print("wallet_balance (btc): %s" % wallet_balance)
      assert wallet_balance > 0

  unittest.main()

  print("Done")
