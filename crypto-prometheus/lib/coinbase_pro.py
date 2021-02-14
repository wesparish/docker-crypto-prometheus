try:
  from cryptobase import CryptoBase
except:
  from .cryptobase import CryptoBase

import logging
import os
import sys
import cbpro

logging.basicConfig(stream=sys.stdout, level=getattr(logging, os.getenv('LOG_LEVEL', 'WARN')))

class CoinbasePro(CryptoBase):
  def __init__(self, currency, key, secret, passphrase):
    super(CoinbasePro, self).__init__('na')
    self._authenticated_client = cbpro.AuthenticatedClient(key, secret, passphrase)
    self._currency = currency

  def get_current_price(self):
    return float(self._authenticated_client.get_product_ticker(
      product_id='%s-USD' % self._currency.upper())['price'])

  def get_wallet_balance(self):
    accounts = self._authenticated_client.get_accounts()
    return float([x for x in accounts if x['currency'] == self._currency.upper()][0]['balance'])

if __name__ == "__main__":
  import os
  print("Testing %s" % (os.path.basename(__file__)))

  cbpro_address = os.getenv('COINBASE_PRO_ADDRESS')
  api_key = cbpro_address.split(':')[0]
  secret = cbpro_address.split(':')[1]
  passphrase = cbpro_address.split(':')[2]

  import unittest
  class TestCoinbasePro(unittest.TestCase):
    def setUp(self):
      self.cbpro = CoinbasePro('btc', api_key, secret, passphrase)

    def tearDown(self):
      pass

    def test_get_price_from_api(self):
      current_price = self.cbpro.get_current_price()
      print("current_price (btc): %s" % current_price)
      assert current_price > 0

    def test_get_wallet_balance(self):
      wallet_balance = self.cbpro.get_wallet_balance()
      print("wallet_balance (btc): %s" % wallet_balance)
      assert wallet_balance > 0

  unittest.main()

  print("Done")