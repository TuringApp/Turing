# -*- coding: utf-8 -*-


class UndoRedo:
    """Helper class for undo-redo operations.

    undo_gen -- function that takes an action and returns the undo function
    redo_gen -- function that takes an action and returns the redo function"""
    history = None
    position = None
    undo_gen = None
    redo_gen = None

    def __init__(self, undo_gen, redo_gen):
        self.history = []
        self.position = 0
        self.undo_gen = undo_gen
        self.redo_gen = redo_gen

    def can_undo(self):
        """Checks if the user can undo an operation."""

        return self.position > 0

    def can_redo(self):
        """Checks if the user can redo an operation."""

        return self.position < len(self.history) - 1

    def undo_act(self):
        """Returns the last action."""

        return self.history[self.position]

    def redo_act(self):
        """Returns the next action."""

        return self.history[self.position + 1]

    def undo(self):
        """Undoes the last action."""

        if not self.can_undo():
            print("error: trying to undo")
            return

        fn = self.undo_gen(self.undo_act())
        fn()
        self.position -= 1

    def redo(self):
        """Redoes the next action."""

        if not self.can_redo():
            print("error: trying to redo")
            return

        fn = self.redo_gen(self.redo_act())
        fn()
        self.position += 1

    def push(self, act):
        """Pushes an action to the stack.

        If the position is not at the end, erases the remaining actions.

        act -- action to push"""

        self.history = self.history[0:self.position]
        self.history.append(act)
