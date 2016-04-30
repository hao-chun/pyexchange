"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
import unittest
from httpretty import HTTPretty, httprettified
import httpretty
from pyexchange import Exchange2010Service

from pyexchange.exchange2010 import Exchange2010Attachment
from pyexchange.connection import ExchangeNTLMAuthConnection
from pyexchange.exceptions import *  # noqa

from .fixtures import *  # noqa

config = {
  "username": FAKE_EXCHANGE_USERNAME,
  "password": FAKE_EXCHANGE_PASSWORD,
  "url": FAKE_EXCHANGE_URL
}


class Test_GettingAnEventWithAttachment(unittest.TestCase):

  @httprettified
  def setUp(self):
    self.calendar = Exchange2010Service(
      connection=ExchangeNTLMAuthConnection(
        **config
      )
    ).calendar()

  def test_sets_up_an_empty_array_if_no_attachments(self):
    httpretty.enable()
    HTTPretty.register_uri(
      HTTPretty.POST,
      FAKE_EXCHANGE_URL,
      body=GET_ITEM_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8'
    )

    event = self.calendar.get_event(id=TEST_EVENT.id)

    assert event.attachments.__len__() == 0

  def test_sets_up_correct_attachment_objects(self):
    httpretty.enable()
    HTTPretty.register_uri(
      HTTPretty.POST,
      FAKE_EXCHANGE_URL,
      body=GET_ITEM_WITH_ATTACHMENTS_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8'
    )

    event = self.calendar.get_event(id=TEST_EVENT.id)

    # Two, as per fixture
    assert event.attachments.__len__() == 2
    # Of type Attachment object
    for x in event.attachments:
      assert type(x) == Exchange2010Attachment
    # With the correct ids
    assert set(ATTACHMENT_IDS) == set([x.id for x in event.attachments])
