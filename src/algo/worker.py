# -*- coding: utf-8 -*-
import time
import typing
from collections import Iterable
from typing import *

from algo.stmts import *
from maths.evaluator import Evaluator
from maths.nodes import *
from maths.parser import Parser
from util import translate
from util.log import Logger

Loops = (ForStmt, WhileStmt)
StackFrame = Tuple[BlockStmt, int]
ExecStack = List[StackFrame]

class Worker:
    code: BlockStmt = None
    stack: ExecStack = None
    evaluator: Evaluator = None
    log: Logger = None
    callback_input: Callable = None
    callback_print: Callable = None
    calls: List[Optional[Any]] = None
    strict_typing: bool = None
    last = None
    callback_stop: Callable = None
    map: Dict[Type[BaseStmt], Callable] = None

    def __init__(self, code: CodeBlock):
        self.code = BlockStmt(code)
        self.log = Logger("Algo")
        self.strict_typing = False
        self.callback_stop = lambda: ()
        self.map = {
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
            SleepStmt: self.exec_sleep
        }

    def reset_eval(self):
        """Resets the worker's evaluator object."""
        self.evaluator = Evaluator()
        self.evaluator.log = self.log
        self.evaluator.strict_typing = self.strict_typing

    def stmt_input(self, prompt: str = None) -> Any:
        """Executes an input statement."""
        if self.callback_input is not None:
            res = self.callback_input(prompt)
        else:
            res = input(prompt)

        p = Parser(str(res))
        return self.evaluator.eval_node(p.parse())

    def stmt_print(self, *args, end="\n"):
        """Executes a print statement."""
        if self.callback_print is not None:
            self.callback_print(*args, end=end)
            return

        print(*args, end=end)

    def iterate_for(self, stmt: ForStmt) -> bool:
        """Updates a for loop."""
        current = self.evaluator.get_variable(stmt.variable)
        step = self.evaluator.eval_node(stmt.step or NumberNode(1))

        current = self.evaluator.binary_operation(current, step, "+")
        self.evaluator.set_variable(stmt.variable, current)

        return self.check_for_condition(stmt, current, step)

    def check_for_condition(self, stmt: ForStmt, current: Any = None, step: Any = None) -> bool:
        """Checks for the condition of a for loop."""
        begin = self.evaluator.eval_node(stmt.begin)
        end = self.evaluator.eval_node(stmt.end)

        condition_1 = bool(self.evaluator.binary_operation(current, begin, "><"[step < 0] + "="))
        condition_2 = bool(self.evaluator.binary_operation(current, end, "<>"[step < 0] + "="))
        return condition_1 and condition_2

    def find_parent(self, types: Union[type, typing.Iterable[type]]) -> Optional[Tuple[int, StackFrame]]:
        """Finds the nearest frame of the specified type."""
        if not isinstance(types, Iterable):
            types = [types]

        for idx, frame in enumerate(reversed(self.stack)):
            if type(frame[0]) in types:
                return idx, frame

        return None

    def next_stmt(self) -> Optional[BaseStmt]:
        """Returns the next statement to be executed."""
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

    def peek_following(self) -> BaseStmt:
        """Returns the immediately following statement. Does not handle loops or functions."""
        stmt, index = self.stack[-1]

        if index + 1 < len(stmt.children):
            return stmt.children[index + 1]

        if len(self.stack) == 1:
            self.finish()
            return None

        return None

    def enter_block(self, stmt: BlockStmt, value=None):
        """Pushes a new frame to the stack."""
        self.stack.append((stmt, -1))
        self.evaluator.enter_frame(value)

    def exit_block(self):
        """Pops the last frame from the stack."""
        self.evaluator.exit_frame()
        return self.stack.pop()

    def exec_display(self, stmt: DisplayStmt):
        """Executes a display statement."""
        self.stmt_print(str(self.evaluator.eval_node(stmt.content)), end="\n" if stmt.newline else "")

    def exec_input(self, stmt: InputStmt):
        """Executes an input statement."""
        prompt = (
            translate("Algo", "Variable {var} = ").format(
                var=stmt.variable.code())) if stmt.prompt is None else self.evaluator.eval_node(stmt.prompt)
        self.assign(stmt.variable, self.stmt_input(prompt))

    def assign(self, target: AstNode, value):
        """Assigns the specified value to the target (either variable or array access)."""
        if isinstance(target, IdentifierNode):
            self.evaluator.set_variable(target.value, value)
        elif isinstance(target, ArrayAccessNode):
            array = self.evaluator.eval_node(target.array)

            if not type(array) == list:
                self.log.error(translate("Algo", "Array access target must be of array type"))
                self.finish()
                return

            index = self.evaluator.eval_node(target.index)

            while index >= len(array):
                array.append(0)

            if index < len(array):
                array[index] = value
            else:
                self.log.error(translate("Algo", "Index '{idx}' too big for array").format(idx=index))
                return None
        else:
            self.log.error(translate("Algo", "Assignment target must be either variable or array item"))
            self.finish()
            return

    def exec_assign(self, stmt: AssignStmt):
        """Executes an  assignment statement."""
        value = None if stmt.value is None else self.evaluator.eval_node(stmt.value)
        self.assign(stmt.variable, value)

    def exec_if(self, stmt: IfStmt):
        """Executes an if block."""
        self.enter_block(stmt)

        condition = bool(self.evaluator.eval_node(stmt.condition))
        self.if_status = (len(self.stack) - 1, condition)

        if not condition:
            self.exit_block()

    def exec_while(self, stmt: WhileStmt):
        """Executes a while loop."""
        self.enter_block(stmt)

        predicate = bool(self.evaluator.eval_node(stmt.condition))
        if not predicate:
            self.exit_block()

    def exec_for(self, stmt: ForStmt):
        """Executes a for loop."""
        self.enter_block(stmt)
        self.evaluator.set_variable(stmt.variable, self.evaluator.eval_node(stmt.begin), local=True)

        if not self.check_for_condition(stmt, self.evaluator.get_variable(stmt.variable),
                                        self.evaluator.eval_node(stmt.step or NumberNode(1))):
            self.exit_block()

    def exec_break(self, stmt: BreakStmt):
        """Executes a break statement."""
        if not self.find_parent(Loops):
            self.log.error(translate("Algo", "BREAK can only be used inside a loop"))
            self.finish()
            return

        while True:
            if isinstance(self.exit_block()[0], Loops):
                break

    def exec_continue(self, stmt: ContinueStmt):
        """Executes a continue statement."""
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
        """Executes a function definition block."""
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
        """Executes a return statement."""
        if not self.find_parent(FuncStmt):
            self.log.error(translate("Algo", "RETURN can only be used inside a function"))
            self.finish()
            return

        self.calls.append(self.evaluator.eval_node(stmt.value) if stmt.value else None)

        while True:
            if isinstance(self.exit_block()[0], FuncStmt):
                break

    def call_function(self, stmt: FuncStmt, *args) -> Optional[Any]:
        """Calls the specified function."""
        self.enter_block(stmt, {stmt.parameters[idx]: arg for idx, arg in enumerate(args)})
        length = len(self.stack)

        while len(self.stack) >= length and not self.finished:
            self.step()

        if len(self.stack) != length - 1:
            self.log.error(translate("Algo", "Stack corruption after calling function %s" % stmt.name))
            return None

        return self.calls.pop()

    def exec_call(self, stmt: CallStmt):
        """Executes a function call statement."""
        self.evaluator.eval_node(stmt.to_node())

    def exec_else(self, stmt: ElseStmt):
        """Executes an else block."""
        if self.if_status is None:
            self.log.error(translate("Algo", "ELSE can only be used after an IF block"))
            self.finish()
            return

        if not self.if_status[1]:
            self.enter_block(stmt)

        self.if_status = None

    def exec_stop(self, stmt: StopStmt):
        """Executes a breakpoint statement."""
        self.stopped = True
        self.callback_stop(stmt)

    def exec_sleep(self, stmt: SleepStmt):
        """Executes a sleep statement"""
        time.sleep(self.evaluator.eval_node(stmt.duration))

    def step(self):
        """Executes a step."""
        stmt = self.next_stmt()
        self.last = stmt
        if stmt is None:
            return

        self.exec_stmt(stmt)

        if self.break_on_error and self.log.messages:
            self.finish()

    def exec_stmt(self, stmt):
        """Executes the specified statement."""
        self.last = stmt

        if self.if_status is not None and type(stmt) != ElseStmt and len(self.stack) <= self.if_status[0]:
            self.if_status = None

        if type(stmt) not in self.map:
            self.log.error(translate("Algo", "Unknown statement type: {type}").format(type=type(stmt)))
            self.finish()
            return

        self.map[type(stmt)](stmt)

    def finish(self, normal=False):
        """Ends the execution."""
        self.finished = True
        self.error = not normal
        self.evaluator.exit_frame()

    def init(self):
        """Initialises the worker."""
        self.reset_eval()
        self.stack = [(self.code, -1)]
        self.calls = []
        self.if_status = None
        self.finished = False
        self.error = False
        self.evaluator.enter_frame()
        self.stopped = False
        self.break_on_error = False

    def run(self):
        """Runs the program continuously."""
        self.init()

        while not self.finished:
            self.step()
