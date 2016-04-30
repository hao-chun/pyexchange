"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
import unittest
from httpretty import HTTPretty, httprettified
import httpretty
from pytest import raises
from pyexchange import Exchange2010Service

from pyexchange.connection import ExchangeNTLMAuthConnection
from pyexchange.exceptions import *  # noqa
from pyexchange.exchange2010 import Exchange2010Attachment

from .fixtures import *  # noqa

config = {
  "username": FAKE_EXCHANGE_USERNAME,
  "password": FAKE_EXCHANGE_PASSWORD,
  "url": FAKE_EXCHANGE_URL
}


class Test_DeletingAnAttachment(unittest.TestCase):
  calendar = None

  def setUp(self):
    httpretty.enable()
    self.service = Exchange2010Service(
      connection=ExchangeNTLMAuthConnection(
        **config
      )
    )

    HTTPretty.register_uri(
      HTTPretty.POST,
      FAKE_EXCHANGE_URL,
      body=GET_ATTACHMENT_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8'
    )

    self.attachment = Exchange2010Attachment(self.service, ATTACHMENT_DETAILS.id, load=True)

  def test_includes_id_into_post(self):
    httpretty.enable()
    HTTPretty.register_uri(
      HTTPretty.POST,
      FAKE_EXCHANGE_URL,
      body=DELETE_ATTACHMENT_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8'
    )
    self.attachment.delete()
    assert ATTACHMENT_DETAILS.id in httpretty.last_request().body
