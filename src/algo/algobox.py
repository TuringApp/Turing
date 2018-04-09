# -*- coding: utf-8 -*-

import builtins
import xml.etree.ElementTree as etree
from typing import Union, Optional

from algo.stmts import *
from maths.nodes import *
from maths.parser import quick_parse as parse
from util import translate


def parse_algobox(xml):
    root = etree.fromstring(xml)
    result = []

    for elem in root:
        r = to_stmt(elem)

        if r is not None:
            if type(r) == list:
                result.extend(r)
            else:
                result.append(r)

    return BlockStmt(result)


def parse_expr(expr):
    lut = {
        "Math.PI": "pi",
        "&&": "&",
        "||": "|"
    }

    for k, v in lut.items():
        expr = expr.replace(k, v)

    return parse(expr)


def get_color(color):
    lut = {
        "Bleu": "blue",
        "Rouge": "red",
        "Vert": "green",
        "Blanc": "white"
    }

    if color not in lut:
        raise ValueError(translate("Algobox", "Unknown color: {color}").format(color=color))

    return lut[color]


def to_stmt(elem) -> Optional[Union[BaseStmt, CodeBlock]]:
    if elem.tag == "description":
        value = elem.attrib["texte"]

        if not value:
            return None

        return [CommentStmt(x) for x in elem.attrib["texte"].replace("\r\n", "\n").split("\n")]

    if elem.tag == "repere":
        if elem.attrib["repetat"] == "inactif":
            return None

        xmin, xmax, ymin, ymax, xgrad, ygrad = elem.attrib["repcode"].split("#")

        return GWindowStmt(parse_expr(xmin), parse_expr(xmax), parse_expr(ymin), parse_expr(ymax), parse_expr(xgrad), parse_expr(ygrad))

    if elem.tag == "fonction":
        if elem.attrib["fctetat"] == "inactif":
            return None

        return AssignStmt(IdentifierNode("F1"), LambdaNode(["x"], parse_expr(elem.attrib["fctcode"])))

    if elem.tag == "item":
        code, *args = elem.attrib["code"].split("#")
        code = int(code)
        children = []

        if len(list(elem)) != 0:
            for e in elem:
                s = to_stmt(e)

                if s is None:
                    continue

                if builtins.type(s) == list:
                    children.extend(s)
                else:
                    children.append(s)

        if code == 1:  # VARIABLE
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

        elif code == 2:  # LIRE
            varname, index = args

            if index == "pasliste":
                return InputStmt(IdentifierNode(varname))

            return InputStmt(ArrayAccessNode(IdentifierNode(varname), parse(index)))

        elif code == 3:  # AFFICHER
            varname, newline, index = args

            if index == "pasliste":
                return DisplayStmt(IdentifierNode(varname), bool(int(newline)))

            return DisplayStmt(ArrayAccessNode(IdentifierNode(varname), parse(index)), bool(int(newline)))

        elif code == 4:  # MESSAGE
            message, newline = args

            return DisplayStmt(StringNode(message), bool(int(newline)))

        elif code == 5:  # AFFECTATION
            varname, value, index = args

            if index == "pasliste":
                return AssignStmt(IdentifierNode(varname), parse_expr(value))

            return AssignStmt(ArrayAccessNode(IdentifierNode(varname), parse_expr(index)), parse_expr(value))

        elif code == 6:  # SI
            condition = args[0]

            if isinstance(children[-1], ElseStmt):
                return [IfStmt(parse_expr(condition), children[:-1]), children[-1]]

            return IfStmt(parse_expr(condition), children)

        elif code == 7:  # DEBUT_SI
            return None

        elif code == 8:  # FIN_SI
            return None

        elif code == 9:  # SINON
            return ElseStmt(children)

        elif code == 10:  # DEBUT_SINON
            return None

        elif code == 11:  # FIN_SINON
            return None

        elif code == 12:  # POUR
            varname, begin, end = args

            return ForStmt(varname, parse_expr(begin), parse_expr(end), children)

        elif code == 13:  # DEBUT_POUR
            return None

        elif code == 14:  # FIN_POUR
            return None

        elif code == 15:  # TANT_QUE
            condition = args[0]

            return WhileStmt(parse_expr(condition), children)

        elif code == 16:  # DEBUT_TANT_QUE
            return None

        elif code == 17:  # FIN_TANT_QUE
            return None

        elif code == 18:  # PAUSE
            return BreakStmt()

        elif code == 19:  # COMMENTAIRE
            value = args[0]

            return CommentStmt(value)

        elif code == 20:  # AFFICHERCALCUL
            calcul, newline = args

            return DisplayStmt(parse_expr(calcul), bool(int(newline)))

        elif code == 50:  # POINT
            x, y, color = args

            return GPointStmt(parse_expr(x), parse_expr(y), StringNode(get_color(color)))

        elif code == 51:  # SEGMENT
            start_x, start_y, end_x, end_y, color = args

            return GLineStmt(parse_expr(start_x), parse_expr(start_y), parse_expr(end_x), parse_expr(end_y), StringNode(get_color(color)))

        elif code == 52:  # EFFACE
            return GClearStmt()

        elif code == 100:  # VARIABLES
            return children

        elif code == 101:  # DEBUT_ALGO
            return children

        elif code == 102:  # FIN_ALGO
            return None

        elif code == 103:  # autres
            pass

        elif code == 200:  # FONCTIONS_UTILISEES
            return children

        elif code == 201:  # FONCTION
            name, params = args

            return FuncStmt(name, [x.strip() for x in params.split(",")], children)

        elif code == 202:  # VARIABLES_FONCTION
            return children

        elif code == 203:  # DEBUT_FONCTION
            return None

        elif code == 204:  # FIN_FONCTION:
            return None

        elif code == 205:  # RENVOYER_FONCTION
            value = args[0]

            return ReturnStmt(parse_expr(value))

        elif code == 206:  # APPELER_FONCTION
            expr = args[0]

            return CallStmt.from_node(parse_expr(expr))

        else:
            print("unknown type %d" % code)
            return None

        print("unimpl type %d" % code)
