BODY_TYPE_BEST = u'Best'
BODY_TYPE_HTML = u'HTML'
BODY_TYPE_TEXT = u'Text'
BODY_TYPES = [BODY_TYPE_BEST, BODY_TYPE_HTML, BODY_TYPE_TEXT]


class BaseExchangeAttachment(object):
  def __init__(self, service, attachment_id, load=False):
    self.service = service
    self.id = attachment_id
    if not load:
      self._loaded = False
    else:
      self.load()

  def _send_soap_request(self, body_type, include_mime_content, filter_html_content):
    raise NotImplementedError

  def _send_delete_request(self):
    raise NotImplementedError

  def _parse_response_for_get_attachment(root):
    raise NotImplementedError

  @property
  def content(self):
    if not self._loaded:
      self.load()
    return self._content

  @property
  def name(self):
    if not self._loaded:
      self.load()
    return self._name

  def delete(self):
    # Normal SOAP error handling should work here
    self._send_delete_request()

  def load(self, body_type=None, include_mime_content=False, filter_html_content=False):
    # Defaults, only valid values
    if body_type not in BODY_TYPES:
      body_type = BODY_TYPE_BEST

    include_mime_content = 'false'
    if include_mime_content is True:
      include_mime_content = 'true'

    filter_html_content = 'false'
    if filter_html_content is True:
      filter_html_content = 'true'

    # Send soap request
    root = self._send_soap_request(body_type, include_mime_content, filter_html_content)
    # Parse it (That'll have to be defined on child classes)
    self._parse_response_for_get_attachment(root)
    self._loaded = True
    return self
