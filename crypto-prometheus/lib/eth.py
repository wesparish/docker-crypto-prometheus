try:
  from cryptobase import CryptoBase
except:
  from .cryptobase import CryptoBase

import logging
import os
import sys

logging.basicConfig(stream=sys.stdout, level=getattr(logging, os.getenv('LOG_LEVEL', 'WARN')))

class Eth(CryptoBase):
  def __init__(self, address):
    super(Eth, self).__init__(address)

  def get_current_price(self):
    value = None
    
    from moneywagon.services import Bittrex
    client = Bittrex()

    while True:
      try:
        value = client.get_current_price('eth', 'usd')
        break
      except Exception as ex:
        print("Caught exception in get_current_price: %s" % ex)
    return value

  def get_wallet_balance(self):
    value = None
    
    from moneywagon.services import Etherscan
    client = Etherscan()

    while True:
      try:
        value = client.get_balance('eth', self._address)
        break
      except Exception as ex:
        print("Caught exception in get_wallet_balance: %s" % ex)
    return value

if __name__ == "__main__":
  import os
  print("Testing %s" % (os.path.basename(__file__)))

  import unittest
  class TestEth(unittest.TestCase):
    def setUp(self):
      address = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
      self.eth = Eth(address)

    def tearDown(self):
      pass

    def test_get_price_from_api(self):
      current_price = self.eth.get_current_price()
      print("current_price (eth): %s" % current_price)
      assert current_price > 0

    def test_get_wallet_balance(self):
      wallet_balance = self.eth.get_wallet_balance()
      print("wallet_balance (eth): %s" % wallet_balance)
      assert wallet_balance > 0

  unittest.main()

  print("Done")