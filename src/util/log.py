# -*- coding: utf-8 -*-

class Logger:
    """Logger class."""

    ERROR, WARNING = range(2)

    context = None
    callback = None
    messages = None

    def __init__(self, context="Log"):
        """Initialises the Logger instance."""
        self.context = context
        self.callback = print
        self.messages = []

    def print(self, msg):
        """Logs the specified message."""
        self.callback("[%s] %s" % (self.context, msg))

    def error(self, msg):
        """Logs the specified error."""
        self.print("[ERROR] %s" % msg)
        self.messages.append((Logger.ERROR, msg))

    def warn(self, msg):
        """Logs the specified warning."""
        self.print("[ WARN] %s" % msg)
        self.messages.append((Logger.WARNING, msg))

    def set_callback(self, cb):
        """Replaces the default printing callback function."""
        self.callback = cb

    def get_messages(self):
        """Fetches the log messages."""
        return self.messages
