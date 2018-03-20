# -*- coding: utf-8 -*-

import maths.nodes as nodes
from algo.stmts import *
from algo.stmts.BreakStmt import BreakStmt
from algo.stmts.ContinueStmt import ContinueStmt
from algo.worker import Worker
from tests.framework import expect
from maths.parser import quick_parse as parse

tests = [
    (
        [
            AssignStmt("sum", parse("0")),
            InputStmt("N"),
            ForStmt("i", parse("1"), parse("N"), [
                AssignStmt("sum", parse("sum + i"))
            ]),
            DisplayStmt(parse("\"Result=\" + sum"))
        ],
        "5",
        [
            "Variable N = 5",
            "Result=15"
        ]
    ),
    (
        [
            ForStmt("i", parse("1"), parse("3"), [
                ForStmt("i", parse("1"), parse("3"), [
                    DisplayStmt(parse("i"))
                ])
            ])
        ],
        "",
        [
            "1",
            "2",
            "3",
            "1",
            "2",
            "3",
            "1",
            "2",
            "3",
        ]
    ),
    (
        [
            AssignStmt("i", parse("42")),
            ForStmt("i", parse("1"), parse("10"), [
                IfStmt(parse("1"), [
                    IfStmt(parse("i % 2"), [
                        ContinueStmt()
                    ]),
                    IfStmt(parse("i > 5"), [
                        FuncStmt("fibo", ["n"], [
                            IfStmt(parse("n <= 1"), [
                                ReturnStmt(parse("n"))
                            ]),
                            ReturnStmt(parse("fibo(n-1)+fibo(n-2)"))
                        ]),
                        DisplayStmt(parse("map(fibo, [5, 7, 9])")),
                        DisplayStmt(parse("i")),
                        BreakStmt()
                    ]),
                    DisplayStmt(parse("i")),
                ])
            ]),
            DisplayStmt(parse("i"))
        ],
        "",
        [
            "2",
            "4",
            "[5, 13, 34]",
            "6",
            "42"
        ]
    )
]


def run_tests():
    for algo, input, exp_output in tests:
        worker = Worker(algo)

        output = ""

        def buffer_print(*args, end="\n"):
            nonlocal output
            output += " ".join(str(arg) for arg in args) + end

        worker.callback_print = buffer_print

        iter_input = iter(input.split("\n"))

        def buffer_input(prompt=""):
            result = next(iter_input)
            buffer_print(prompt + result)
            return result

        worker.callback_input = buffer_input

        worker.evaluator.strict_typing = True
        worker.run()

        expect(output, "".join(x + "\n" for x in exp_output))
