from logging import info
from lxml import etree


class Base:
    """Base class for all others."""

    def __init__(self, action: etree.Element, target):
        self._action: etree.Element = action
        self._target = target

    def _info(self, method):
        info(method.__doc__)
        info(f'action={etree.tostring(self._action)}')
        info(f'target={etree.tostring(self._target)}')
