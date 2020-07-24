from logging import info
from lxml import etree

from xml_patch.utils import is_attribute_node, is_text_node, has_no_child_element
from xml_patch.exceptions.invalid_node_types import InvalidNodeTypes


class Base:
    """Base class for all others."""

    def __init__(self, action: etree.Element, target):
        self._action: etree.Element = action
        self._target = target

    def _info(self, method):
        info(method.__doc__)
        info(f'action={etree.tostring(self._action)}')
        if isinstance(self._target, list):
            info('target=[')
            for elem in self._target:
                if etree.iselement(elem):
                    info(etree.tostring(elem))
                else:
                    info(f'"{elem}"')
            info(']')
        elif isinstance(self._target, str):
            info(f'target={self._target}')
        else:
            if etree.iselement(self._target):
                info(f'target={etree.tostring(self._target)}')
            else:
                info(f'target={self._target}')

    def _guard_text_action(self):
        if not has_no_child_element(self._action):
            raise InvalidNodeTypes(self._action)
