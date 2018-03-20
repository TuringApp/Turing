# -*- coding: utf-8 -*-

from typing import Tuple, List, Callable


class LogType:
    ERROR, WARNING = range(2)


LogMessage = Tuple[LogType, str]


class Logger:
    """Logger class."""

    context: str = None
    callback: Callable = None
    messages: List[LogMessage] = None

    def __init__(self, context="Log"):
        """Initialises the Logger instance."""
        self.context = context
        self.callback = print
        self.messages = []

    def print(self, msg: str):
        """Logs the specified message."""
        self.callback("[%s] %s" % (self.context, msg))

    def error(self, msg: str):
        """Logs the specified error."""
        self.print("[ERROR] %s" % msg)
        self.messages.append((LogType.ERROR, msg))

    def warn(self, msg: str):
        """Logs the specified warning."""
        self.print("[ WARN] %s" % msg)
        self.messages.append((LogType.WARNING, msg))

    def set_callback(self, cb: Callable):
        """Replaces the default printing callback function."""
        self.callback = cb

    def get_messages(self) -> List[LogMessage]:
        """Fetches the log messages."""
        return self.messages
