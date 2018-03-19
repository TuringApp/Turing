# -*- coding: utf-8 -*-


def centered(content):
    """Returns the HTML code for a centered container."""
    return '<div style="text-align: center; display: flex; flex-direction: column">%s</div>' % content

def color_span(text, color):
	return '<span style="color: %s">%s</span>' % (color, text)