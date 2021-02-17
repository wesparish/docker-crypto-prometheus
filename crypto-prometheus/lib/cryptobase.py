from abc import ABC, abstractmethod
import csv
import sys
import datetime
import logging
import os
import time

logging.basicConfig(stream=sys.stdout, level=getattr(logging, os.getenv('LOG_LEVEL', 'WARN')))

class CryptoBase(ABC):
  def __init__(self, address):
    self._address = address
    self._query_loops = 3

  @abstractmethod
  def get_current_price(self):
    pass

  @abstractmethod
  def get_wallet_balance(self):
    pass