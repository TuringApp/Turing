# -*- coding: utf-8 -*-
import typing
from collections import Iterable
from typing import Optional, Union

from algo.stmts import *
from maths.evaluator import Evaluator
from maths.nodes import *
from maths.parser import Parser
from util import translate
from util.log import Logger

Loops = (ForStmt, WhileStmt)


class Worker:
    code = None
    stack = None
    evaluator = None
    log = None
    callback_input = None
    callback_print = None
    calls = None
    strict_typing = None
    last = None
    stop_callback = None

    def __init__(self, code: CodeBlock):
        self.code = BlockStmt(code)
        self.log = Logger("Algo")
        self.strict_typing = False
        self.stop_callback = lambda: ()

    def reset_eval(self):
        self.evaluator = Evaluator()
        self.evaluator.strict_typing = self.strict_typing

    def stmt_input(self, prompt: str = None):
        if self.callback_input is not None:
            res = self.callback_input(prompt)
        else:
            res = input(prompt)

        p = Parser(res)
        return self.evaluator.eval_node(p.parse())

    def stmt_print(self, *args, end="\n"):
        if self.callback_print is not None:
            self.callback_print(*args, end=end)
            return

        print(*args, end=end)

    def iterate_for(self, stmt: ForStmt):
        current = self.evaluator.get_variable(stmt.variable)
        step = self.evaluator.eval_node(stmt.step or NumberNode(1))

        current = self.evaluator.binary_operation(current, step, "+")
        self.evaluator.set_variable(stmt.variable, current)

        return self.check_for_condition(stmt, current, step)

    def check_for_condition(self, stmt: ForStmt, current=None, step=None):
        begin = self.evaluator.eval_node(stmt.begin)
        end = self.evaluator.eval_node(stmt.end)

        condition_1 = bool(self.evaluator.binary_operation(current, begin, "><"[step < 0] + "="))
        condition_2 = bool(self.evaluator.binary_operation(current, end, "<>"[step < 0] + "="))
        return condition_1 and condition_2

    def find_parent(self, types: Union[type, typing.Iterable[type]]):
        if not isinstance(types, Iterable):
            types = [types]

        for idx, frame in enumerate(reversed(self.stack)):
            if type(frame[0]) in types:
                return idx, frame

        return None

    def next_stmt(self) -> Optional[BaseStmt]:
        while True:
            stmt, index = self.stack[-1]
            index += 1

            if index >= len(stmt.children):
                if len(self.stack) == 1:
                    self.finish(True)
                    return None

                if isinstance(stmt, ForStmt):
                    if self.iterate_for(stmt):
                        self.stack[-1] = (stmt, -1)
                        continue

                elif isinstance(stmt, WhileStmt):
                    if bool(self.evaluator.eval_node(stmt.condition)):
                        self.stack[-1] = (stmt, -1)
                        continue

                elif isinstance(stmt, FuncStmt):
                    self.calls.append(None)
                    self.exit_block()
                    return None

                self.exit_block()
                continue

            break

        self.stack[-1] = (stmt, index)

        return stmt.children[index]

    def peek_following(self):
        stmt, index = self.stack[-1]

        if index + 1 < len(stmt.children):
            return stmt.children[index + 1]

        if len(self.stack) == 1:
            self.finish()
            return None

        return None

    def enter_block(self, stmt: BlockStmt, value=None):
        self.stack.append((stmt, -1))
        self.evaluator.enter_frame(value)

    def exit_block(self):
        self.evaluator.exit_frame()
        return self.stack.pop()

    def exec_display(self, stmt: DisplayStmt):
        self.stmt_print(str(self.evaluator.eval_node(stmt.content)))

    def exec_input(self, stmt: InputStmt):
        prompt = (
            translate("Algo", "Variable {var} = ").format(var=stmt.variable)) if stmt.prompt is None else stmt.prompt
        self.evaluator.set_variable(stmt.variable, self.stmt_input(prompt))

    def exec_assign(self, stmt: AssignStmt):
        self.evaluator.set_variable(stmt.variable, None if stmt.value is None else self.evaluator.eval_node(stmt.value))

    def exec_if(self, stmt: IfStmt):
        self.enter_block(stmt)

        condition = bool(self.evaluator.eval_node(stmt.condition))
        self.if_status = (len(self.stack) - 1, condition)

        if not condition:
            self.exit_block()

    def exec_while(self, stmt: WhileStmt):
        self.enter_block(stmt)

        predicate = bool(self.evaluator.eval_node(stmt.condition))
        if not predicate:
            self.exit_block()

    def exec_for(self, stmt: ForStmt):
        self.enter_block(stmt)
        self.evaluator.set_variable(stmt.variable, self.evaluator.eval_node(stmt.begin), local=True)

        if not self.check_for_condition(stmt, self.evaluator.get_variable(stmt.variable),
                                        self.evaluator.eval_node(stmt.step or NumberNode(1))):
            self.exit_block()

    def exec_break(self, stmt: BreakStmt):
        if not self.find_parent(Loops):
            self.log.error(translate("Algo", "BREAK can only be used inside a loop"))
            self.finish()
            return

        while True:
            if isinstance(self.exit_block()[0], Loops):
                break

    def exec_continue(self, stmt: ContinueStmt):
        if not self.find_parent(Loops):
            self.log.error(translate("Algo", "CONTINUE can only be used inside a loop"))
            self.finish()
            return

        while not isinstance(self.stack[-1][0], Loops):
            self.exit_block()
        stmt, index = self.stack[-1]
        index = len(stmt.children)
        self.stack[-1] = stmt, index

    def exec_function(self, stmt: FuncStmt):
        parent_func = self.find_parent(FuncStmt)
        frames = [x.copy() for x in self.evaluator.frames[1:]]

        def wrapper(*args):
            for frame in frames:
                self.evaluator.enter_frame(frame)

            result = self.call_function(stmt, *list(args))

            for frame in frames:
                self.evaluator.exit_frame()

            return result

        self.evaluator.set_variable(stmt.name, wrapper)

    def exec_return(self, stmt: ReturnStmt):
        if not self.find_parent(FuncStmt):
            self.log.error(translate("Algo", "RETURN can only be used inside a function"))
            self.finish()
            return

        self.calls.append(self.evaluator.eval_node(stmt.value) if stmt.value else None)

        while True:
            if isinstance(self.exit_block()[0], FuncStmt):
                break

    def call_function(self, stmt: FuncStmt, *args):
        self.enter_block(stmt, {stmt.parameters[idx]: arg for idx, arg in enumerate(args)})
        length = len(self.stack)

        while len(self.stack) >= length and not self.finished:
            self.step()

        if len(self.stack) != length - 1:
            self.log.error(translate("Algo", "Stack corruption after calling function %s" % stmt.name))
            return None

        return self.calls.pop()

    def exec_call(self, stmt: CallStmt):
        self.evaluator.eval_node(stmt.to_node())

    def exec_else(self, stmt: ElseStmt):
        if self.if_status is None:
            self.log.error(translate("Algo", "ELSE can only be used after an IF block"))
            self.finish()
            return

        if not self.if_status[1]:
            self.enter_block(stmt)

        self.if_status = None

    def exec_stop(self, stmt: StopStmt):
        self.stopped = True
        self.stop_callback()

    def step(self):
        stmt = self.next_stmt()
        self.last = stmt
        if stmt is None:
            return

        self.exec_stmt(stmt)

    def exec_stmt(self, stmt):
        self.last = stmt

        map = {
            DisplayStmt: self.exec_display,
            InputStmt: self.exec_input,
            AssignStmt: self.exec_assign,
            IfStmt: self.exec_if,
            ForStmt: self.exec_for,
            WhileStmt: self.exec_while,
            BreakStmt: self.exec_break,
            ContinueStmt: self.exec_continue,
            FuncStmt: self.exec_function,
            ReturnStmt: self.exec_return,
            CallStmt: self.exec_call,
            ElseStmt: self.exec_else,
            BaseStmt: lambda _: (),
            CommentStmt: lambda _: (),
            StopStmt: self.exec_stop,
        }

        if self.if_status is not None and type(stmt) != ElseStmt and len(self.stack) <= self.if_status[0]:
            self.if_status = None

        if type(stmt) not in map:
            self.log.error(translate("Algo", "Unknown statement type: {type}").format(type=type(stmt)))
            self.finish()
            return

        map[type(stmt)](stmt)

    def finish(self, normal=False):
        self.finished = True
        self.error = not normal
        self.evaluator.exit_frame()

    def init(self):
        self.reset_eval()
        self.stack = [(self.code, -1)]
        self.calls = []
        self.if_status = None
        self.finished = False
        self.error = False
        self.evaluator.enter_frame()
        self.stopped = False

    def run(self):
        self.init()

        while not self.finished:
            self.step()
