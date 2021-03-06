#  GPLv3 https://www.gnu.org/licenses/gpl-3.0.en.html
#
#  Author: eidng8
#

from lxml import etree

from xml_patch.base import Base
from xml_patch.exceptions.invalid_node_types import InvalidNodeTypes
from xml_patch.exceptions.unlocated_node import UnlocatedNode
from xml_patch.utils import is_attribute_node, is_text_node


class ActionReplace(Base):
    """Handles the `<replace>` directive (action).
    Please note that `CDATA` if present, are treated as plain text nodes,
    with only their contents.

    RFC document excerpt:
    ------

    4.4.  `<replace>` Element
    ======
    The `<replace>` element represents a replacement operation: for
    example, an existing element is updated with a new element or an
    attribute value is replaced with a new value.  This `<replace>`
    operation always updates a single node or node content at a time.

    The `<replace>` element type only has a 'sel' attribute.  If the
    located target node is an element, a comment or a processing
    instruction, then the child of the `<replace>` element MUST also be of
    the same type.  Otherwise, the `<replace>` element MUST have text
    content or it MAY be empty when replacing an attribute value or a
    text node content.
    """

    def apply(self):
        """Apply the given replace action on target."""
        self._info(ActionReplace.apply)
        if isinstance(self._target, list):
            if 1 == len(self._target):
                self._target = self._target[0]
            else:
                raise UnlocatedNode(self._action)
        self._apply()

    def _apply(self):
        """Apply the given replace action on only one target."""
        self._info(ActionReplace._apply)
        if isinstance(self._target, str):
            if is_attribute_node(self._target):
                self._handle_attribute()
            elif is_text_node(self._target):
                self._handle_text()
            else:
                raise UnlocatedNode(self._action, 'Invalid target')
        elif etree.iselement(self._target):
            self._handle_element()
        else:
            raise UnlocatedNode(self._action, 'Invalid target')

    def _handle_element(self):
        """Apply the given replace action on target element.
        This method is called when `etree.iselement(self._target)` is `True`.
        This includes elements, comments, and processing instructions.
        """
        self._info(ActionReplace._handle_element)
        if len(self._action) != 1:
            raise InvalidNodeTypes(self._action)
        replacement = self._action[0]
        """The number of child nodes has been restricted to one by schema."""
        if self._target.tag is etree.Comment:
            if replacement.tag is not etree.Comment:
                raise InvalidNodeTypes(self._action)
        elif self._target.tag is etree.PI:
            if replacement.tag is not etree.PI:
                raise InvalidNodeTypes(self._action)
        else:
            if self._target.tail:
                replacement.tail = self._target.tail
        self._target.getparent().replace(self._target, replacement)

    def _handle_attribute(self):
        """Apply the given replace action on target attribute."""
        self._info(ActionReplace._handle_attribute)
        self._guard_text_action()
        replacement = self._action.text
        sel: str = self._action.get('sel')
        pos = sel.index('@') + 1
        attr_name = sel[pos:]
        self._target.getparent().set(attr_name, replacement)

    def _handle_text(self):
        """Apply the given replace action on target text content."""
        self._info(ActionReplace._handle_text)
        self._guard_text_action()
        self._target.getparent().text = self._action.text
