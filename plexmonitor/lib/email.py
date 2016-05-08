import imaplib  # type: ignore
import re
from email.message import Message
from email.parser import Parser
from typing import Tuple, List, Union, Any

from plexmonitor.settings import IMAP

ImapSearchResponseType = Tuple[str, List[bytes]]

# imaplib.fetch() returns a tuple, the second element is a list containing:
#     1. A Tuple of 3 elements:
#         1.1 bytes
#         1.2 bytes
#         1.3 bytes
#     2. bytes
# The typing module only allows List to be of a single type. This is perfectly
# logical, unlike imaplib which is a bunch of dogshit. To avoid this steaming
# pile of shit, just do List[Any] so that the mixed types are allowed
ImapFetchResponseType = Tuple[str, List[Any]]


def get_sender_email(mail: Message) -> str:
    """ Retrieve the sender's email address from a Message object
    """
    sender_pattern = re.compile("^(?P<name>.*)\s<(?P<email>.*)>$")
    from_header = mail['From']  # type: str

    sender = sender_pattern.match(from_header)
    if not sender:
        raise KeyError("Invalid From header on email")

    return sender.group('email')


class Inbox:
    """ Interface with an IMAP inbox
    """
    def __init__(self):
        self.server = IMAP['server']      # type: str
        self.port = IMAP['port']          # type: int
        self.email_addr = IMAP['email']   # type: str
        self.password = IMAP['password']  # type: str
        self.conn = None                  # type: imaplib.IMAP4_SSL

    def connect(self):
        """ Instantiate an IMAP SSL connection as read only
        """
        self.conn = imaplib.IMAP4_SSL(self.server, self.port)
        self.conn.login(self.email_addr, self.password)
        self.conn.select(readonly=True)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        pass

    def _decode_fetch_response(self, resp: ImapFetchResponseType) -> Message:
        """ Take a raw IMAP RFC822 fetch response and decode the data portion
        """
        _, data = resp
        actual_data = data[0][1].decode()  # type: str

        parser = Parser()
        msg = parser.parsestr(actual_data)
        return msg

    def _decode_search_response(self, resp: ImapSearchResponseType) -> str:
        """ Take a raw IMAP search response and decode the data portion
        """
        _, data = resp
        return data[0].decode()

    def fetch(self, mail_id: str) -> Message:
        resp = self.conn.fetch(mail_id, '(RFC822)')
        return self._decode_fetch_response(resp)

    def search(self, criteria: List[str]) -> str:
        """ Perform a search using the supplied search criteria. This method
        applies criteria only to the address specified in the settings file
        """
        search_params = ['TO', self.email_addr]
        search_params.extend(criteria)
        search_str = ' '.join(search_params)

        resp = self.conn.search(None, search_str)
        return self._decode_search_response(resp)

    def get_all_unread_mail_ids(self) -> List[str]:
        mail_ids = self.search(['UNSEEN'])
        mail_ids = mail_ids.split()
        return mail_ids

    def get_last_unread_mail_id(self) -> str:
        return self.get_all_unread_mail_ids()[-1]

