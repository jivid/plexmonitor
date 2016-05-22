from functools import wraps
from typing import Callable, Any, Union

from plexmonitor.lib.command import Command

# TODO(divij): I can't yet figure out what the return type of handler functions
# should be, so just use Any for now
HandlerFuncType = Callable[[Command], Any]

__all__ = ['get_handler_for_action']

_registry = {}  # type: Dict[str, HandlerFuncType]


def get_handler_for_action(action: str) -> Union[HandlerFuncType, None]:
    """ Get a handler from the registry
    """
    return _registry.get(action)


def handles(action: str) -> Callable[[HandlerFuncType], Any]:
    """ Simple decorator to add a function to the handler registry. It takes as
    an argument the action the function handles.

    If many functions handle the same action, only the first is registered
    """
    def wrapper(func: HandlerFuncType):
        @wraps(func)
        def wrapped_func(command: Command):
            if not isinstance(command, Command):
                raise RuntimeError("{} is not an instance of Command"
                                    .format(command))
            return func(command)

        # Register just the first function and ensure that the wrapped
        # function is registered, not the raw one
        if action not in _registry:
            _registry[action] = wrapped_func

        return wrapped_func
    return wrapper


@handles('status')
def get_system_status(cmd):
    print("Checking system status")
