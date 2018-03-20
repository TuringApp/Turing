# -*- coding: utf-8 -*-

from algo.stmts import *
from maths.evaluator import Evaluator
from maths.parser import Parser
from util.log import Logger
import algo.stmts as stmts

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

    def stmt_input(self, prompt = None):
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

    def next_stmt(self):
        while True:
            node, index = self.current[-1]
            index += 1

            if index >= len(node.children):
                if len(self.current) == 1:
                    self.finished = True
                    return None

                if type(node) == ForStmt:
                    # update counter
                    current = self.evaluator.get_variable(node.variable)
                    step = self.evaluator.eval_node(node.step)
                    current = self.evaluator.binary_operation(current, step, "+")
                    self.evaluator.set_variable(node.variable, current)

                    # check condition
                    begin = self.evaluator.eval_node(node.begin)
                    end = self.evaluator.eval_node(node.end)

                    condition_1 = bool(self.evaluator.binary_operation(current, begin, "><"[step < 0] + "="))
                    condition_2 = bool(self.evaluator.binary_operation(current, end, "<>"[step < 0] + "="))
                    condition = condition_1 and condition_2

                    if condition:
                        index = 0
                    else:
                        self.current.pop()
                        continue

            break

        self.current[-1] = (node, index)
        return node.children[index]

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
                condition = bool(self.evaluator.eval_node(stmt.condition))
                if condition:
                    self.current.append((stmt, -1))

            if isinstance(stmt, WhileStmt):
                predicate = bool(self.evaluator.eval_node(stmt.predicate))
                if predicate:
                    self.current.append((stmt, -1))

            if isinstance(stmt, ForStmt):
                self.evaluator.set_variable(stmt.variable, self.evaluator.eval_node(stmt.begin))
                self.current.append((stmt, -1))



    def run(self):
        self.current = [(self.code, -1)]
        self.evaluator.variables = {}
        while not self.finished:
            self.step()
        print("finished")
