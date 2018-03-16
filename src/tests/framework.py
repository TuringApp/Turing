# -*- coding: utf-8 -*-

from util.math import isnum, isclose


def init_test():
    """Inits the testing environment."""
    global test_results, test_stack, current_results
    test_results = []
    test_stack = []
    current_results = []


def begin_test(name):
    """Begins testing for the specified component.

    name -- Identifier for the component"""
    test_stack.append(name)
    print("[STAT] Beginning tests for '%s'" % name)


def end_test(name):
    """Ends testing for the specified environment.

    name -- Identifier for the component"""
    if test_stack[-1] != name:
        raise ValueError("Trying to pop the wrong value on the stack (got %s, expected %s)" % (name, test_stack[-1]))

    test_stack.pop()

    test_results.append((name, list(current_results)))
    n_total = len(current_results)
    n_passed = sum(1 for x in current_results if x[0])
    n_failed = n_total - n_passed
    print("[STAT] Ending tests for '%s' - [%d passed, %d failed] / %d total" % (name, n_passed, n_failed, n_total))
    current_results.clear()


def expect(x, expec, info=""):
    """Standard unit testing function. Asserts that two values are equal.

    x     -- Given value
    expec -- Value that is to be expected
    info  -- [Optional] additional information about the unit test"""
    if isnum(x) and isnum(expec):
        val = isclose(x, expec)
    else:
        val = (x == expec)

    if val:
        stat = "PASSED"
        msg = "(value : '%s')" % str(expec)
    else:
        stat = "FAILED"
        msg = "(expected: '%s', got: '%s')" % (str(expec), str(x))

    print("[TEST] #%02d : %s %s%s" % (len(current_results) + 1, stat, msg, " | " + info if info else ""))

    current_results.append((val, x, expec, info))


def show_summary():
    """Shows the summary of all tests, shows stats for each test group."""
    for grp, res in test_results:
        n_total = len(res)
        n_passed = sum(1 for x in res if x[0])
        n_failed = n_total - n_passed
        print("[STAT] Results for '%s' : %d%% [%d passed, %d failed] / %d total" % (
            grp, n_passed / n_total * 100, n_passed, n_failed, n_total))
