# -*- coding: utf-8 -*-

from algo.stmts import *
from maths.evaluator import Evaluator
from maths.parser import Parser
from util import translate
from util.log import Logger


class Worker():
    code = None
    current = None
    evaluator = None
    log = None
    finished = None
    callback_input = None
    callback_print = None

    def __init__(self, code: CodeBlock):
        self.code = BlockStmt(code)
        self.current = []
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

    def next_stmt(self) -> Optional[BaseStmt]:
        while True:
            stmt, index = self.current[-1]
            index += 1

            if index >= len(stmt.children):
                if len(self.current) == 1:
                    self.finished = True
                    return None

                if isinstance(stmt, ForStmt):
                    if self.iterate_for(stmt):
                        index = 0
                    else:
                        self.current.pop()
                        self.evaluator.exit_frame()
                        continue

            break

        self.current[-1] = (stmt, index)
        return stmt.children[index]

    def enter_block(self, stmt: BlockStmt):
        self.current.append((stmt, -1))
        self.evaluator.enter_frame()

    def exit_block(self):
        self.evaluator.exit_frame()
        return self.current.pop()

    def step(self):
        stmt = self.next_stmt()

        if stmt is None:
            return

        if type(stmt) == DisplayStmt:
            self.stmt_print(str(self.evaluator.eval_node(stmt.content)))

        elif type(stmt) == InputStmt:
            prompt = (translate("Algorithm", "Variable %s = ") % stmt.variable) if stmt.prompt is None else stmt.prompt
            self.evaluator.set_variable(stmt.variable, self.stmt_input(prompt))

        elif type(stmt) == AssignStmt:
            self.evaluator.set_variable(stmt.variable, self.evaluator.eval_node(stmt.value))

        elif isinstance(stmt, BlockStmt):
            if isinstance(stmt, IfStmt):
                self.enter_block(stmt)

                condition = bool(self.evaluator.eval_node(stmt.condition))
                if not condition:
                    self.exit_block()

            if isinstance(stmt, WhileStmt):
                self.enter_block(stmt)

                predicate = bool(self.evaluator.eval_node(stmt.predicate))
                if not predicate:
                    self.exit_block()

            if isinstance(stmt, ForStmt):
                self.enter_block(stmt)
                self.evaluator.set_variable(stmt.variable, self.evaluator.eval_node(stmt.begin), local=True)

                if not self.check_for_condition(stmt, self.evaluator.get_variable(stmt.variable),
                                            self.evaluator.eval_node(stmt.step)):
                    self.exit_block()

        elif isinstance(stmt, BreakStmt):
            while True:
                if isinstance(self.exit_block()[0], (ForStmt, WhileStmt)):
                    break

        elif isinstance(stmt, ContinueStmt):
            while not isinstance(self.current[-1][0], (ForStmt, WhileStmt)):
                self.exit_block()
            stmt, index = self.current[-1]
            index = len(stmt.children)
            self.current[-1] = stmt, index

    def run(self):
        self.current = [(self.code, -1)]
        self.evaluator.enter_frame()
        while not self.finished:
            self.step()
        self.evaluator.exit_frame()
        print("finished")
