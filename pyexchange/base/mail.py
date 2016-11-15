BODY_TYPE_HTML = u'HTML'
BODY_TYPE_TEXT = u'Text'
BODY_TYPES = [BODY_TYPE_HTML, BODY_TYPE_TEXT]

import email
import six
import logging
log = logging.getLogger('pyexchange')

class BaseExchangeEmailService(object):
  email_class = None
  def __init__(self, service):
    self.service = service

  def _send_get_mailboxes_request(self):
      raise NotImplementedError

  def get_mailboxes(self):
    raise NotImplementedError('Below doesnt work for the time being')
    root = self._send_get_mailboxes_request()

  def send(self, subject, body, recipients, cc_recipients=[], bcc_recipients=[], body_type=BODY_TYPE_HTML):
    if self.email_class is None:
      raise NotImplementedError

    email = self.email_class(self.service, None)
    return email.send(subject, body, recipients, cc_recipients, bcc_recipients, body_type)

class BaseExchangeEmail(object):
    email_id = None
    def __init__(self, service, email_id):
        self.service = service
        self.email_id = email_id

    def _send_soap_request(self, subject, body, recipients, cc_recipients, bcc_recipients, body_type):
      raise NotImplementedError

    def _send_delete_request(self):
      raise NotImplementedError

    def _parse_create_response(self, root):
      raise NotImplementedError

    def delete(self):
      # Normal SOAP error handling should work here
      self._send_delete_request()

    def send(self, subject, body, recipients, cc_recipients=[], bcc_recipients=[], body_type=BODY_TYPE_HTML):
      """
        List of recipients (and CC and BCC) are expected to be a list of either strings or tuples ('name', 'email_address')
      """
      for list_of_recipients in (recipients, cc_recipients, bcc_recipients):
          for i, recipient in enumerate(list_of_recipients):
              if isinstance(recipient, six.string_types):
                  list_of_recipients[i] = email.utils.parseaddr(recipient)
              elif not isinstance(recipient, tuple):
                  raise ValueError('Invalid email format: %s' % recipient)
      log.info('Sending email to recipients: {main}, CC to {cc}, BCC to {bcc}'.format(main=recipients, cc=cc_recipients, bcc=bcc_recipients))
      outcome = self._send_soap_request(subject, body, recipients, cc_recipients, bcc_recipients, body_type)
      if outcome is None:
          log.info('Email sent successfully')
      else:
          log.error('An error occurred while sending email: %s' % outcome)
      return outcome
