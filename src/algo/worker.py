# -*- coding: utf-8 -*-
from typing import Optional

from algo.stmts import *
from algo.stmts.BlockStmt import BlockStmt
from algo.stmts.BreakStmt import BreakStmt
from algo.stmts.ContinueStmt import ContinueStmt
from maths.evaluator import Evaluator
from maths.parser import Parser
from util import translate
from util.log import Logger


class Worker():
    code = None
    stack = None
    evaluator = None
    log = None
    finished = None
    callback_input = None
    callback_print = None

    def __init__(self, code: CodeBlock):
        self.code = BlockStmt(code)
        self.stack = []
        self.log = Logger("Algo")
        self.finished = False
        self.reset_eval()

    def reset_eval(self):
        self.evaluator = Evaluator()

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
        step = self.evaluator.eval_node(stmt.step)

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
                return (idx, frame)

        return None

    def next_stmt(self) -> Optional[BaseStmt]:
        while True:
            stmt, index = self.stack[-1]
            index += 1

            if index >= len(stmt.children):
                if len(self.stack) == 1:
                    self.finished = True
                    return None

                if isinstance(stmt, ForStmt):
                    if self.iterate_for(stmt):
                        self.stack[-1] = (stmt, -1)
                        continue

                elif isinstance(stmt, WhileStmt):
                    if bool(self.evaluator.eval_node(stmt.predicate)):
                        self.stack[-1] = (stmt, -1)
                        continue

                self.exit_block()
                continue

            break

        self.stack[-1] = (stmt, index)

        return stmt.children[index]

    def enter_block(self, stmt: BlockStmt):
        self.stack.append((stmt, -1))
        self.evaluator.enter_frame()

    def exit_block(self):
        self.evaluator.exit_frame()
        return self.stack.pop()

    def exec_display(self, stmt: DisplayStmt):
        self.stmt_print(str(self.evaluator.eval_node(stmt.content)))

    def exec_input(self, stmt: InputStmt):
        prompt = (translate("Algorithm", "Variable %s = ") % stmt.variable) if stmt.prompt is None else stmt.prompt
        self.evaluator.set_variable(stmt.variable, self.stmt_input(prompt))

    def exec_assign(self, stmt: AssignStmt):
        self.evaluator.set_variable(stmt.variable, self.evaluator.eval_node(stmt.value))

    def exec_if(self, stmt: IfStmt):
        self.enter_block(stmt)

        condition = bool(self.evaluator.eval_node(stmt.condition))
        if not condition:
            self.exit_block()

    def exec_while(self, stmt: WhileStmt):
        self.enter_block(stmt)

        predicate = bool(self.evaluator.eval_node(stmt.predicate))
        if not predicate:
            self.exit_block()

    def exec_for(self, stmt: ForStmt):
        self.enter_block(stmt)
        self.evaluator.set_variable(stmt.variable, self.evaluator.eval_node(stmt.begin), local=True)

        if not self.check_for_condition(stmt, self.evaluator.get_variable(stmt.variable),
                                        self.evaluator.eval_node(stmt.step)):
            self.exit_block()

    def exec_break(self, stmt: BreakStmt):
        if not self.find_parent(Loops):
            self.log.error(translate("Algo", "BREAK can only be used inside a loop"))
            self.finished = True
            return
        while True:
            if isinstance(self.exit_block()[0], (ForStmt, WhileStmt)):
                break

    def exec_continue(self, stmt: ContinueStmt):
        while not isinstance(self.stack[-1][0], (ForStmt, WhileStmt)):
        if not self.find_parent(Loops):
            self.log.error(translate("Algo", "CONTINUE can only be used inside a loop"))
            self.finished = True
            return
            self.exit_block()
        stmt, index = self.stack[-1]
        index = len(stmt.children)
        self.stack[-1] = stmt, index

    def step(self):
        stmt = self.next_stmt()

        if stmt is None:
            return

        map = {
            DisplayStmt: self.exec_display,
            InputStmt: self.exec_input,
            AssignStmt: self.exec_assign,
            IfStmt: self.exec_if,
            ForStmt: self.exec_for,
            WhileStmt: self.exec_while,
            BreakStmt: self.exec_break,
            ContinueStmt: self.exec_continue
        }

        if type(stmt) not in map:
            self.log.error(translate("Algo", "Unknown statement type: %s") % type(stmt))
            self.finished = True
            return

        map[type(stmt)](stmt)

    def run(self):
        self.stack = [(self.code, -1)]
        self.evaluator.enter_frame()
        while not self.finished:
            self.step()
        self.evaluator.exit_frame()
        print("finished")
