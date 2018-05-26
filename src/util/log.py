# -*- coding: utf-8 -*-

from typing import Tuple, List, Callable


class LogType:
    ERROR, WARNING = range(2)


LogMessage = Tuple[LogType, str]


class Logger:
    """Logger class."""

    def __init__(self, context="Log"):
        """Initialises the Logger instance."""
        self.context = context
        self.callback = print
        self.messages = []
        self.use_prefix = True

    def print(self, msg: str):
        """Logs the specified message."""
        if self.use_prefix:
            self.callback("[%s] %s" % (self.context, msg))
        else:
            self.callback(msg)

    def error(self, msg: str):
        """Logs the specified error."""
        if self.use_prefix:
            self.print("[ERROR] %s" % msg)
        else:
            self.print(msg)
        self.messages.append((LogType.ERROR, msg))

    def warn(self, msg: str):
        """Logs the specified warning."""
        if self.use_prefix:
            self.print("[ WARN] %s" % msg)
        else:
            self.print(msg)
        self.messages.append((LogType.WARNING, msg))

    def set_callback(self, cb: Callable):
        """Replaces the default printing callback function."""
        self.callback = cb

    def get_messages(self) -> List[LogMessage]:
        """Fetches the log messages."""
        return self.messages

    def has_errors(self) -> bool:
        return any(msg for msg in self.messages if msg[0] == LogType.ERROR)
