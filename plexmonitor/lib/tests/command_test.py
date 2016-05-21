import re
import unittest
from unittest.mock import Mock, patch

from plexmonitor.lib.command import Command


class CommandTest(unittest.TestCase):
    def test_regex(self):
        """ Test that the regex() method returns a pattern matcher
        """
        regex = Command.regex()
        self.assertIsInstance(regex, re._pattern_type)

    def test_regex_lru_cache(self):
        """ Test that the regex() method's output is cached
        """
        regex = Command.regex()

        with patch('re.compile') as mock_compile:
            mock_compile.return_value = False
            regex2 = Command.regex()

            self.assertEqual(regex, regex2)
            mock_compile.assert_not_called()

    def test_from_email_no_subject(self):
        """ Test that a missing subject line just returns None
        """
        mail = {}
        cmd = Command.from_email(mail)
        self.assertIsNone(cmd)

    def test_from_email_invalid_command(self):
        """ Test that an invalid command in the subject line just returns None
        """
        mail = {'Subject': 'foo bar'}
        cmd = Command.from_email(mail)
        self.assertIsNone(cmd)

    def test_from_email_invalid_sender(self):
        """ Test that an exception while retrieving the sender's email address
        returns None
        """
        cmd_str = ' '.join([Command.CMD_PREFIX, Command.VALID_ACTIONS[0]])
        mail = {'Subject': cmd_str}

        with patch('plexmonitor.lib.command.get_sender_email') as mock_sender:
            mock_sender.side_effect = [RuntimeError]
            cmd = Command.from_email(mail)
            self.assertIsNone(cmd)

    def test_from_email_valid_commands(self):
        """ Test that a valid command in the email's subject line yields a
        properly instantiated Command object with an action and context
        """
        fake_email = 'foo_email'

        def make_mail(action):
            return {'Subject': ' '.join([Command.CMD_PREFIX, action]),
                    'From': fake_email}

        with patch('plexmonitor.lib.command.get_sender_email') as mock_sender:
            mock_sender.return_value = fake_email

            for action in Command.VALID_ACTIONS:
                mail = make_mail(action)
                cmd = Command.from_email(mail)
                self.assertIsInstance(cmd, Command)
                self.assertEqual(cmd.action, action)
                self.assertEqual(cmd.context['sender'], fake_email)

    def test_str(self):
        cmd = Command(action='foo')
        self.assertEqual(str(cmd), '<Command: foo>')

    def test_repr(self):
        cmd = Command(action='foo')
        self.assertEqual(repr(cmd), str(cmd))
