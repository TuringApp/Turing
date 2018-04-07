# -*- coding: utf-8 -*-

import xml.etree.ElementTree as etree

import builtins
from typing import Union

from algo.stmts import *
from maths.nodes import *
from util import translate
from maths.parser import quick_parse as parse

def parse_algobox(xml):
    root = etree.fromstring(xml)
    result = []

    for elem in root:
        r = to_stmt(elem)

        if r is not None:
            result.append(r)

    return BlockStmt(result)


def parse_expr(expr):
    return parse(expr)


def to_stmt(elem) -> Union[BaseStmt, CodeBlock]:
    if elem.tag == "description":
        return CommentStmt(elem.attrib["texte"])

    if elem.tag == "fonction":
        if elem.attrib["fctetat"] == "inactif":
            return None
        print("shit")

    if elem.tag == "item":
        code, *args = elem.attrib["code"].split("#")
        code = int(code)
        children = []

        if len(list(elem)) != 0:
            for e in elem:
                s = to_stmt(e)

                if builtins.type(s) == list:
                    children.extend(s)
                else:
                    children.append(s)

        if code == 1: # VARIABLE
            type, varname = args

            value = None

            if type == "NOMBRE":
                value = NumberNode(0)
            elif type == "CHAINE":
                value = StringNode("")
            elif type == "LISTE":
                value = ListNode([])

            if value is None:
                raise ValueError(translate("Algobox", "Unknown variable type: {type}").format(type=type))

            return AssignStmt(IdentifierNode(varname), value)

        elif code == 2: # LIRE
            varname, index = args

            if index == "pasliste":
                return InputStmt(IdentifierNode(varname))

            return [InputStmt(ArrayAccessNode(IdentifierNode(varname), NumberNode(int(index))))]

        elif code == 3: # AFFICHER
            varname, newline, index = args

        elif code == 4: # MESSAGE
            message, newline = args

            return DisplayStmt(StringNode(message), bool(int(newline)))

        elif code == 5: # AFFECTATION
            varname, value, index = args

        elif code == 6: # SI
            condition = args[0]

            return IfStmt(parse_expr(condition), children)

        elif code == 7: # DEBUT_SI
            pass

        elif code == 8: # FIN_SI
            pass

        elif code == 9: # SINON
            return ElseStmt(children)

        elif code == 10: # DEBUT_SINON
            pass

        elif code == 11: # FIN_SINON
            pass

        elif code == 12: # POUR
            varname, begin, end = args

            return ForStmt(varname, parse_expr(begin), parse_expr(end), children)

        elif code == 13: # DEBUT_POUR
            pass

        elif code == 14: # FIN_POUR
            pass

        elif code == 15: # TANT_QUE
            condition = args[0]

            return WhileStmt(parse_expr(condition), children)

        elif code == 16: # DEBUT_TANT_QUE
            pass

        elif code == 17: # FIN_TANT_QUE
            pass

        elif code == 18: # PAUSE
            return BreakStmt()

        elif code == 19: # COMMENTAIRE
            value = args[0]

            return CommentStmt(value)

        elif code == 20: # AFFICHERCALCUL
            calcul, newline = args

            return DisplayStmt(parse_expr(calcul), bool(int(newline)))

        elif code == 50: # POINT
            x, y, color = args

        elif code == 51: # SEGMENT
            start_x, start_y, end_x, end_y, color = args

        elif code == 52: # EFFACE
            pass

        elif code == 100: # DECLARATIONS VARIABLES
            return children

        elif code == 101: # DEBUT_ALGO
            pass

        elif code == 102: # FIN_ALGO
            pass

        elif code == 103: # autres
            pass
