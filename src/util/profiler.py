# -*- coding: utf-8 -*-
import inspect
from datetime import datetime
import os

# disable for releases
ENABLE_PROFILER = True

points = []

# https://gist.github.com/sadikovi/8a2b9a472729f17f387cb53ffbdcbee6

def table(rows, margin=0, columns=[]):
    """
    Return string representing table content, returns table as string and as a list of strings.
    It is okay for rows to have different sets of keys, table will show union of columns with
    missing values being empty spaces.
    :param rows: list of dictionaries as rows
    :param margin: left space padding to apply to each row, default is 0
    :param columns: extract listed columns in provided order, other columns will be ignored
    :return: table content as string and as list
    """
    def projection(cols, columns):
        return [(x, cols[x]) for x in columns if x in cols] if columns else cols.items()
    def row_to_string(row, columns):
        values = [(row[name] if name in row else "").rjust(size) for name, size in columns]
        return "|%s|" % ("|".join(values))
    def header(columns):
        return "|%s|" % ("|".join([name.rjust(size) for name, size in columns]))
    def divisor(columns):
        return "+%s+" % ("+".join(["-" * size for name, size in columns]))
    data = [dict([(str(a), str(b)) for a, b in row.items()]) for row in rows]
    cols = dict([(x, len(x) + 1) for row in data for x in row.keys()]) if data else {}
    for row in data:
        for key in row.keys():
            cols[key] = max(cols[key], len(row[key]) + 1)
    proj = projection(cols, columns) # extract certain columns to display (or all if not provided)
    table = [divisor(proj), header(proj), divisor(proj)] + \
        [row_to_string(row, proj) for row in data] + [divisor(proj)]
    table = ["%s%s" % (" " * margin, tpl) for tpl in table] if margin > 0 else table
    table_text = "\n".join(table)
    return (table_text, table)


def show(rows, margin=0, columns=[]):
    """
    Print table in console for list of rows.
    """
    txt, _ = table(rows, margin, columns)
    print(txt)


def pf_point(name="~"):
    if not ENABLE_PROFILER:
        return

    points.append((datetime.now(), (name, inspect.getframeinfo(inspect.currentframe().f_back))))


def pf_end():
    if not ENABLE_PROFILER:
        return

    deltas = []

    for point, prev in zip(points[1:], points):
        deltas.append((point[0] - prev[0], point[1]))

    rows = []

    for (dt, (name, info)) in deltas:
        row = {"id": len(rows), "time": dt, "name": name}
        row["file"], row["line"], row["func"], _, _ = info
        row["file"] = os.path.basename(row["file"])
        rows.append(row)

    rows = reversed(sorted(rows, key=lambda x: x["time"]))

    show(rows, columns=["id", "name", "file", "line", "func", "time"])