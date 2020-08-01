#  GPLv3 https://www.gnu.org/licenses/gpl-3.0.en.html
#
#  Author: eidng8

from lxml import etree


class BaseError(Exception):
    def __init__(self, action, message: str):
        self.message = message
        self.action = etree.tostring(action, pretty_print=True)
