# -*- coding: utf-8 -*-

from util.math import is_num, is_close


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
    num_total = len(current_results)
    num_passed = sum(1 for x in current_results if x[0])
    num_failed = num_total - num_passed
    print(
        "[STAT] Ending tests for '%s' - [%d passed, %d failed] / %d total" % (name, num_passed, num_failed, num_total))
    current_results.clear()

def good_str(x):
    return repr(str(x))[1:-1]

def expect(x, expec, info=""):
    """Standard unit testing function. Asserts that two values are equal.

    x     -- Given value
    expec -- Value that is to be expected
    info  -- [Optional] additional information about the unit test"""
    if is_num(x) and is_num(expec):
        value = is_close(x, expec)
    else:
        value = (x == expec)

    if value:
        stat = "PASSED"
        msg = "(value : '%s')" % good_str(expec)
    else:
        stat = "FAILED"
        msg = "(expected: '%s', got: '%s')" % (good_str(expec), good_str(x))

    print("[TEST] #%02d : %s %s%s" % (len(current_results) + 1, stat, msg, " | " + info if info else ""))

    current_results.append((value, x, expec, info))


def show_summary():
    """Shows the summary of all tests, shows stats for each test group."""
    for group_name, results in test_results:
        num_total = len(results)
        num_passed = sum(1 for x in results if x[0])
        num_failed = num_total - num_passed
        print("[STAT] Results for '%s' : %d%% [%d passed, %d failed] / %d total" %
              (
                  group_name,
                  num_passed / num_total * 100,
                  num_passed,
                  num_failed,
                  num_total
              )
              )
