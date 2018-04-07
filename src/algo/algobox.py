# -*- coding: utf-8 -*-

import xml.etree.ElementTree as etree
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


def to_stmt(elem):
    if elem.tag == "description":
        return CommentStmt(elem.attrib["texte"])

    if elem.tag == "fonction":
        if elem.attrib["fctetat"] == "inactif":
            return None
        print("shit")

    if elem.tag == "item":
        code, *args = elem.attrib["code"].split("#")
        code = int(code)
        if len(list(elem)) != 0:
            # block
            children = []
            for e in elem:
                s = to_stmt(e)

                if type(s) == list:
                    children.extend(s)
                else:
                    children.append(s)

        if code == 1: # VARIABLE
            typ, name = args

            val = None

            if typ == "NOMBRE":
                val = NumberNode(0)
            elif typ == "CHAINE":
                val = StringNode("")
            elif typ == "LISTE":
                val = ListNode([])

            if val is None:
                raise ValueError(translate("Algobox", "Unknown variable type: {type}").format(type=typ))

            return AssignStmt(IdentifierNode(name), val)

        if code == 2: # LIRE
            var, liste = args

            if liste == "pasliste":
                return InputStmt(var)

            return [InputStmt("__input__"), AssignStmt(ArrayAccessNode(IdentifierNode(var), NumberNode(int(liste))), IdentifierNode("__input__"))]

