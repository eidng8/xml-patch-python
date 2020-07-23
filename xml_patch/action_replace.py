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
            else:
                raise UnlocatedNode(self._action)
        self._apply()

    def _apply(self):
        """Apply the given replace action on only one target"""
        self._info(ActionReplace._apply)
        if isinstance(self._target, str):
            if hasattr(self._target, 'is_attribute') and self._target.is_attribute:
                self._handle_attribute()
            elif hasattr(self._target, 'is_text') and self._target.is_text:
                self._handle_text()
            else:
                raise UnlocatedNode(self._action, 'Invalid target')
        elif etree.iselement(self._target):
            self._handle_element()
        else:
            raise UnlocatedNode(self._action, 'Invalid target')

    def _handle_element(self):
        """Apply the given replace action on target element"""
        self._info(ActionReplace._handle_element)
        # number of child elements has been restricted by schema
        replacement = self._action.getchildren()
        if not replacement:
            raise InvalidNodeTypes(self._action)
        replacement = replacement[0]
        if self._target.tail:
            replacement.tail = self._target.tail
        self._target.getparent().replace(self._target, replacement)

    def _handle_attribute(self):
        """Apply the given replace action on target attribute"""
        self._info(ActionReplace._handle_attribute)
        self._guard_text_action()
        replacement = self._action.text
        sel: str = self._action.get('sel')
        pos = sel.index('@') + 1
        attr_name = sel[pos:]
        self._target.getparent().set(attr_name, replacement)

    def _handle_text(self):
        """Apply the given replace action on target text content"""
        self._info(ActionReplace._handle_text)
        self._guard_text_action()
        self._target.getparent().text = self._action.text

    def _guard_text_action(self):
        if self._action.getchildren():
            raise InvalidNodeTypes(self._action)
