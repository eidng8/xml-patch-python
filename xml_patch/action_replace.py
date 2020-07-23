from lxml import etree
from xml_patch.base import Base
from xml_patch.exceptions.invalid_patch_directive import InvalidPatchDirective
from xml_patch.exceptions.invalid_node_types import InvalidNodeTypes
from xml_patch.exceptions.unlocated_node import UnlocatedNode


class ActionReplace(Base):
    """Handles the `<replace>` action."""

    def apply(self):
        """Apply the given replace action on target"""
        self._info(ActionReplace.apply)
        if isinstance(self._target, list):
            if 1 == len(self._target):
                self._target = self._target[0]
                self.handle_element()
            else:
                raise UnlocatedNode(self._action)
        elif isinstance(self._target, str):
            if self._target.is_attribute:
                self.handle_attribute()
            elif self._target.is_text:
                self.handle_text()
            else:
                raise UnlocatedNode(self._action, 'Invalid target')
        elif etree.iselement(self._target):
            self.handle_element()
        else:
            raise UnlocatedNode(self._action, 'Invalid target')

    def handle_element(self):
        """Apply the given replace action on target element"""
        self._info(ActionReplace.handle_element)
        replacement = self._action.getchildren()[0]
        if not etree.iselement(replacement):
            raise InvalidNodeTypes(self._action)
        if self._target.tail:
            replacement.tail = self._target.tail
        self._target.getparent().replace(self._target, replacement)

    def handle_attribute(self):
        """Apply the given replace action on target attribute"""
        self._info(ActionReplace.handle_attribute)
        replacement = self._action.getchildren()[0]
        if not isinstance(replacement, str):
            raise InvalidNodeTypes(self._action)
        attr_name = self._action['sel'][self._action.find('@'):]
        self._target.getparent()[attr_name] = replacement

    def handle_text(self):
        """Apply the given replace action on target text content"""
        self._info(ActionReplace.handle_text)
        replacement = self._action.getchildren()[0]
        if not isinstance(replacement, str):
            raise InvalidNodeTypes(self._action)
        self._target.getparent().text = replacement
