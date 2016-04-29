"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
import unittest
from httpretty import HTTPretty, httprettified
from pyexchange import Exchange2010Service

from pyexchange.exchange2010 import Exchange2010Attachment
from pyexchange.connection import ExchangeNTLMAuthConnection
from pyexchange.exceptions import *  # noqa

import logging
logger = logging.getLogger("pyexchange")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

from .fixtures import *  # noqa

config = {
  "username": FAKE_EXCHANGE_USERNAME,
  "password": FAKE_EXCHANGE_PASSWORD,
  "url": FAKE_EXCHANGE_URL,
}


class Test_GettingAnAttachment(unittest.TestCase):
  calendar = None

  @classmethod
  def setUpClass(cls):
    cls.service = Exchange2010Service(
      connection=ExchangeNTLMAuthConnection(
        **config
      )
    )

  @httprettified
  def test_can_get_attachment(self):
    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=GET_ATTACHMENT_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )
    att = Exchange2010Attachment(self.service, ATTACHMENT_DETAILS.id)
    assert att.content == ATTACHMENT_DETAILS.content
    assert att.name == ATTACHMENT_DETAILS.name

  @httprettified
  def test_gets_sort_of_lazy_loaded(self):
    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=GET_ATTACHMENT_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )
    att = Exchange2010Attachment(self.service, ATTACHMENT_DETAILS.id)
    assert att._loaded is False
    # Simply causes to load
    att.content
    assert att._loaded is True
