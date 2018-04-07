# -*- coding: utf-8 -*-
import html


def centered(content: str) -> str:
    """Returns the HTML code for a centered container."""
    return '<div style="text-align: center; display: flex; flex-direction: column">%s</div>' % content


def color_span(text: str, color: str) -> str:
    return '<span style="color: %s">%s</span>' % (color, text)


def sanitize(text: str) -> str:
    return escape_brackets(html.escape(text, False))


def escape_brackets(text: str) -> str:
    return text.replace("[", "&lbrack;").replace("]", "&rbrack;")


def unescape_brackets(text: str) -> str:
    return text.replace("&lbrack;", "[").replace("&rbrack;", "]")