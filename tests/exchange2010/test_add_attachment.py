"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
import unittest
from httpretty import HTTPretty, httprettified
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


class Test_AddingAnAttachment(unittest.TestCase):
  calendar = None

  @httprettified
  def setUp(self):
    self.calendar = Exchange2010Service(
      connection=ExchangeNTLMAuthConnection(
        **config
      )
    ).calendar()

    HTTPretty.register_uri(
      HTTPretty.POST,
      FAKE_EXCHANGE_URL,
      body=GET_ITEM_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8'
    )

    self.event = self.calendar.get_event(id=TEST_EVENT_ATTACHED.id)
    self.event._change_key = TEST_EVENT_ATTACHED.change_key

  @httprettified
  def test_can_add_from_valid_base64(self):
    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=CREATE_ATTACHMENT_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )
    att = self.event.add_attachment(ATTACHMENT_NAME, b64_data=VALID_BASE64)

    # Should be an attachment
    assert isinstance(att, Exchange2010Attachment)
    # Shouldn't be loaded
    assert att._loaded is False

  @httprettified
  def test_can_add_from_file_like_object(self):
    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=CREATE_ATTACHMENT_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )
    self.event.add_attachment(ATTACHMENT_NAME, file=READABLE_FILE)

  @httprettified
  def test_should_call_update_key_if_not_available(self):
    # TODO pick a mock library instead
    m = self.event.refresh_change_key
    calls = []

    def been_called():
      calls.append('Called it!')
      self.event._change_key = TEST_EVENT_ATTACHED.change_key

    self.event.refresh_change_key = been_called
    self.event._change_key = None
    HTTPretty.register_uri(
      HTTPretty.POST, FAKE_EXCHANGE_URL,
      body=CREATE_ATTACHMENT_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )

    self.event.add_attachment(ATTACHMENT_NAME, file=READABLE_FILE)
    # Put back to original
    self.event.refresh_change_key = m

    assert calls.__len__() > 0

  def test_cant_add_to_not_yet_created_event(self):
    self.event._id = None
    with raises(TypeError):
        self.event.add_attachment('name', b64_data=VALID_BASE64)

  def test_cant_have_empty_name(self):
    with raises(ValueError):
      self.event.add_attachment('', b64_data=VALID_BASE64)

  def test_needs_either_file_or_b64(self):
    with raises(ValueError):
      self.event.add_attachment(ATTACHMENT_NAME)

  def test_fails_with_invalid_base64(self):
    with raises(TypeError):
      self.event.add_attachment(ATTACHMENT_NAME, b64_data=INVALID_BASE64)

  def test_fails_with_non_existing_file(self):
    with raises(IOError):
      self.event.add_attachment(ATTACHMENT_NAME, file='some_random_file_name')
