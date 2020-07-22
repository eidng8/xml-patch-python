from logging import info
from lxml import etree


class ActionReplace:
    """Handles the `<replace>` action."""

    def __init__(self, action: etree.Element, target):
        self._action: etree.Element = action
        self._target = target

    def apply(self):
        """Apply the given replace action on target"""
        self._info(ActionReplace.apply)
        if isinstance(self._target, list):
            if 1 == len(self._target):
                self._target = self._target[0]
                self.handle_element()
            else:
                raise Exception('cannot be list')
        elif isinstance(self._target, str):
            if self._target.is_attribute:
                self.handle_attribute()
            elif self._target.is_text:
                self.handle_text()
            else:
                raise Exception('unsupported data type', self._target)
        elif etree.iselement(self._target):
            self.handle_element()
        else:
            raise Exception('unsupported data type', self._target)

    def handle_element(self):
        """Apply the given replace action on target element"""
        self._info(ActionReplace.handle_element)
        replacement: etree.Element = self._action.getchildren()[0]
        if self._target.tail:
            replacement.tail = self._target.tail
        self._target.getparent().replace(self._target, replacement)

    def handle_attribute(self):
        """Apply the given replace action on target attribute"""
        self._info(ActionReplace.handle_attribute)

    def handle_text(self):
        """Apply the given replace action on target text content"""
        self._info(ActionReplace.handle_text)

    def _info(self, method):
        info(method.__doc__)
        info(f'action={etree.tostring(self._action)}')
        info(f'target={etree.tostring(self._target)}')
