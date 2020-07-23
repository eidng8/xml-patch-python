from lxml import etree


class BaseError(Exception):
    def __init__(self, action, message: str):
        self.message = message
        self.action = etree.tostring(action, pretty_print=True)
