# -*- coding: utf-8 -*-


def centered(content: str) -> str:
    """Returns the HTML code for a centered container."""
    return '<div style="text-align: center; display: flex; flex-direction: column">%s</div>' % content

def color_span(text: str, color: str) -> str:
	return '<span style="color: %s">%s</span>' % (color, text)