# -*- coding: utf-8 -*-

import xml.etree.ElementTree as etree

def to_stmt(xml):
    root = etree.fromstring(xml)
