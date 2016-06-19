import unittest
from unittest.mock import patch

from plexmonitor import handlers


class BaseHandlerTestCase(unittest.TestCase):
    def setUp(self):
        # Need to set clear=True since the registry gets populated on import
        patcher = patch.dict(handlers._registry, clear=True)
        self.addCleanup(patcher.stop)
        patcher.start()


class GetHandlerForActionTestCase(BaseHandlerTestCase):
    def test_get_handler_for_action_returns_none(self):
        """ If no valid handler is registered, then None should be returned
        """
        action = 'blah'
        handler = handlers.get_handler_for_action(action)
        self.assertIsNone(handler)

    def test_get_handler_for_action_checks_registry(self):
        """ The function in the registry should be returned
        """
        def mock_func():
            pass

        action = 'blah'
        handlers._registry[action] = mock_func
        handler = handlers.get_handler_for_action(action)
        self.assertEqual(handler, mock_func)


class HandlesDecoratorTestCase(BaseHandlerTestCase):
    def test_handles_adds_wrapped_function_to_registry(self):
        action = 'blah'

        @handlers.handles(action)
        def mock_func(cmd):
            pass

        handler = handlers.get_handler_for_action(action)
        self.assertEqual(handler, mock_func)

    def test_handles_adds_first_function_to_registry(self):
        action = 'blah'

        @handlers.handles(action)
        def mock_func(cmd):
            pass

        @handlers.handles(action)
        def mock_func2(cmd):
            pass

        handler = handlers.get_handler_for_action(action)
        self.assertEqual(handler, mock_func)

    def test_handles_raises_on_invalid_command(self):
        action = 'blah'

        @handlers.handles(action)
        def mock_func(cmd):
            pass

        with self.assertRaises(RuntimeError):
            handler = handlers.get_handler_for_action(action)
            handler('foo')
