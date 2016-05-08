import re
from email.message import Message
from functools import lru_cache
from typing import Union

from plexmonitor.lib.email import get_sender_email


class Command:
    """ The base command structure for the system. At the very least, a command
    contains an action, and additional context in the form of a dictionary
    """
    CMD_PREFIX = 'plex'
    CMD_PATTERN = "^{prefix}\s(?P<action>{actions})$"
    VALID_ACTIONS = [
        'status',  # Return the current system status
    ]

    def __init__(self, action: str, context: dict = None) -> None:
        self.action = action
        self.context = context

    @classmethod
    def from_email(cls, mail: Message) -> Union[None, Command]:
        subject = mail.get('Subject')  # type: str
        if not subject:
            return None

        match = cls.regex().match(subject.strip())
        if not match:
            return None

        try:
            sender = get_sender_email(mail)
        except Exception:
            return None

        action = match.group('action').strip()
        context = {'sender': sender}
        return cls(action, context)

    @classmethod
    @lru_cache()
    def regex(cls):
        actions_str = '|'.join(cls.VALID_ACTIONS)
        pattern = cls.CMD_PATTERN.format(prefix=cls.CMD_PREFIX,
                                         actions=actions_str)
        return re.compile(pattern)

    def __str__(self):
        return "<Command: {action}>".format(action=self.action)

    def __repr__(self):
        return str(self)

